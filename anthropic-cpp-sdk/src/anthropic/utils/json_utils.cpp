#include "anthropic/utils/json_utils.hpp"
#include "anthropic/types/errors.hpp"
#include <rapidjson/writer.h>
#include <rapidjson/stringbuffer.h>

namespace anthropic {
namespace utils {

std::string json_to_string(const rapidjson::Value& value) {
    rapidjson::StringBuffer buffer;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buffer);
    value.Accept(writer);
    return std::string(buffer.GetString(), buffer.GetSize());
}

rapidjson::Document string_to_json(const std::string& json_str) {
    rapidjson::Document doc;
    rapidjson::ParseResult result = doc.Parse(json_str.c_str());

    if (!result) {
        throw BadRequestError(
            std::string("JSON parse error: ") +
            rapidjson::GetParseError_En(result.Code()) +
            " at offset " + std::to_string(result.Offset())
        );
    }

    return doc;
}

bool has_field(const rapidjson::Value& obj, const char* key) {
    return obj.IsObject() && obj.HasMember(key) && !obj[key].IsNull();
}

std::optional<std::string> get_optional_string(const rapidjson::Value& obj, const char* key) {
    if (!has_field(obj, key)) {
        return std::nullopt;
    }

    if (!obj[key].IsString()) {
        return std::nullopt;
    }

    return std::string(obj[key].GetString());
}

std::optional<int> get_optional_int(const rapidjson::Value& obj, const char* key) {
    if (!has_field(obj, key)) {
        return std::nullopt;
    }

    if (!obj[key].IsInt()) {
        return std::nullopt;
    }

    return obj[key].GetInt();
}

std::optional<double> get_optional_double(const rapidjson::Value& obj, const char* key) {
    if (!has_field(obj, key)) {
        return std::nullopt;
    }

    if (!obj[key].IsNumber()) {
        return std::nullopt;
    }

    return obj[key].GetDouble();
}

std::optional<bool> get_optional_bool(const rapidjson::Value& obj, const char* key) {
    if (!has_field(obj, key)) {
        return std::nullopt;
    }

    if (!obj[key].IsBool()) {
        return std::nullopt;
    }

    return obj[key].GetBool();
}

std::string get_required_string(const rapidjson::Value& obj, const char* key) {
    if (!obj.IsObject() || !obj.HasMember(key)) {
        throw BadRequestError(std::string("Missing required field: ") + key);
    }

    if (!obj[key].IsString()) {
        throw BadRequestError(std::string("Field is not a string: ") + key);
    }

    return std::string(obj[key].GetString());
}

int get_required_int(const rapidjson::Value& obj, const char* key) {
    if (!obj.IsObject() || !obj.HasMember(key)) {
        throw BadRequestError(std::string("Missing required field: ") + key);
    }

    if (!obj[key].IsInt()) {
        throw BadRequestError(std::string("Field is not an integer: ") + key);
    }

    return obj[key].GetInt();
}

double get_required_double(const rapidjson::Value& obj, const char* key) {
    if (!obj.IsObject() || !obj.HasMember(key)) {
        throw BadRequestError(std::string("Missing required field: ") + key);
    }

    if (!obj[key].IsNumber()) {
        throw BadRequestError(std::string("Field is not a number: ") + key);
    }

    return obj[key].GetDouble();
}

bool get_required_bool(const rapidjson::Value& obj, const char* key) {
    if (!obj.IsObject() || !obj.HasMember(key)) {
        throw BadRequestError(std::string("Missing required field: ") + key);
    }

    if (!obj[key].IsBool()) {
        throw BadRequestError(std::string("Field is not a boolean: ") + key);
    }

    return obj[key].GetBool();
}

} // namespace utils
} // namespace anthropic
