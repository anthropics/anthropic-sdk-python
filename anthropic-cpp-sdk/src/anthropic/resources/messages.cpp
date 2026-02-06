#include "anthropic/resources/messages.hpp"
#include "anthropic/client.hpp"
#include "anthropic/types/errors.hpp"
#include "anthropic/utils/json_utils.hpp"
#include <rapidjson/document.h>
#include <rapidjson/writer.h>
#include <rapidjson/stringbuffer.h>

namespace anthropic {
namespace resources {

Messages::Messages(Client& client)
    : client_(client) {
}

std::string Messages::build_request_body(const MessageCreateParams& params) {
    rapidjson::Document doc;
    doc.SetObject();
    auto& allocator = doc.GetAllocator();

    // Required fields
    doc.AddMember("model", rapidjson::Value(params.model.c_str(), allocator), allocator);
    doc.AddMember("max_tokens", params.max_tokens, allocator);

    // Messages array
    rapidjson::Value messages_array(rapidjson::kArrayType);
    for (const auto& msg : params.messages) {
        rapidjson::Value message_obj(rapidjson::kObjectType);
        message_obj.AddMember("role", rapidjson::Value(msg.role.c_str(), allocator), allocator);
        message_obj.AddMember("content", rapidjson::Value(msg.content.c_str(), allocator), allocator);
        messages_array.PushBack(message_obj, allocator);
    }
    doc.AddMember("messages", messages_array, allocator);

    // Optional fields
    if (params.system.has_value()) {
        doc.AddMember("system", rapidjson::Value(params.system->c_str(), allocator), allocator);
    }

    if (params.temperature.has_value()) {
        doc.AddMember("temperature", *params.temperature, allocator);
    }

    if (params.top_p.has_value()) {
        doc.AddMember("top_p", *params.top_p, allocator);
    }

    if (params.top_k.has_value()) {
        doc.AddMember("top_k", *params.top_k, allocator);
    }

    if (params.stop_sequences.has_value() && !params.stop_sequences->empty()) {
        rapidjson::Value stop_array(rapidjson::kArrayType);
        for (const auto& stop : *params.stop_sequences) {
            stop_array.PushBack(rapidjson::Value(stop.c_str(), allocator), allocator);
        }
        doc.AddMember("stop_sequences", stop_array, allocator);
    }

    doc.AddMember("stream", params.stream, allocator);

    // Serialize to string
    return utils::json_to_string(doc);
}

types::Message Messages::parse_response(const std::string& response_body) {
    rapidjson::Document doc = utils::string_to_json(response_body);

    types::Message message;

    // Parse required fields
    message.id = utils::get_required_string(doc, "id");
    message.type = utils::get_required_string(doc, "type");
    message.role = utils::get_required_string(doc, "role");
    message.model = utils::get_required_string(doc, "model");

    // Parse content array
    if (doc.HasMember("content") && doc["content"].IsArray()) {
        for (const auto& block : doc["content"].GetArray()) {
            std::string block_type = utils::get_required_string(block, "type");

            if (block_type == "text") {
                types::TextBlock text_block;
                text_block.type = "text";
                text_block.text = utils::get_required_string(block, "text");
                message.content.push_back(text_block);
            }
            // TODO: Parse other block types (thinking, tool_use, etc.)
        }
    }

    // Parse stop_reason
    if (auto stop_reason_str = utils::get_optional_string(doc, "stop_reason")) {
        message.stop_reason = types::stop_reason_from_string(*stop_reason_str);
    }

    message.stop_sequence = utils::get_optional_string(doc, "stop_sequence");

    // Parse usage
    if (doc.HasMember("usage") && doc["usage"].IsObject()) {
        const auto& usage_obj = doc["usage"];
        message.usage.input_tokens = utils::get_required_int(usage_obj, "input_tokens");
        message.usage.output_tokens = utils::get_required_int(usage_obj, "output_tokens");
        message.usage.cache_creation_input_tokens = utils::get_optional_int(usage_obj, "cache_creation_input_tokens");
        message.usage.cache_read_input_tokens = utils::get_optional_int(usage_obj, "cache_read_input_tokens");
        message.usage.inference_geo = utils::get_optional_string(usage_obj, "inference_geo");
        message.usage.service_tier = utils::get_optional_string(usage_obj, "service_tier");
    }

    return message;
}

types::Message Messages::create(const MessageCreateParams& params) {
    // Build request
    http::Request request;
    request.method = "POST";
    request.url = client_.base_url() + "/v1/messages";
    request.body = build_request_body(params);
    request.timeout_ms = 600000;  // 10 minutes

    // Execute with retry logic
    int attempt = 0;
    const int max_retries = 2;

    while (true) {
        try {
            // Execute HTTP request
            http::Response response = client_.http_client().execute(request);

            // Check for errors
            if (response.status_code >= 400) {
                auto error = create_api_error(response.status_code, "API request failed", response.body);

                // Check if we should retry
                if (client_.retry_policy().should_retry(response.status_code, attempt) && attempt < max_retries) {
                    auto delay = client_.retry_policy().calculate_delay(attempt);
                    std::this_thread::sleep_for(delay);
                    attempt++;
                    continue;
                }

                throw *error;
            }

            // Parse successful response
            return parse_response(response.body);

        } catch (const APIError&) {
            // API errors shouldn't be retried beyond what we already checked
            throw;
        } catch (const std::exception&) {
            // Network errors might be retryable
            if (attempt < max_retries) {
                auto delay = client_.retry_policy().calculate_delay(attempt);
                std::this_thread::sleep_for(delay);
                attempt++;
                continue;
            }
            throw;
        }
    }
}

} // namespace resources
} // namespace anthropic
