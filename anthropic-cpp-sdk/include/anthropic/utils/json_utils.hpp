#pragma once

#include <string>
#include <optional>
#include <vector>
#include <rapidjson/document.h>
#include <rapidjson/writer.h>
#include <rapidjson/stringbuffer.h>
#include <rapidjson/error/en.h>

namespace anthropic {
namespace utils {

// Convert JSON value to string
std::string json_to_string(const rapidjson::Value& value);

// Parse string to JSON document
rapidjson::Document string_to_json(const std::string& json_str);

// Safe optional field access
std::optional<std::string> get_optional_string(const rapidjson::Value& obj, const char* key);
std::optional<int> get_optional_int(const rapidjson::Value& obj, const char* key);
std::optional<double> get_optional_double(const rapidjson::Value& obj, const char* key);
std::optional<bool> get_optional_bool(const rapidjson::Value& obj, const char* key);

// Required field access (throws if missing)
std::string get_required_string(const rapidjson::Value& obj, const char* key);
int get_required_int(const rapidjson::Value& obj, const char* key);
double get_required_double(const rapidjson::Value& obj, const char* key);
bool get_required_bool(const rapidjson::Value& obj, const char* key);

// Check if field exists and is not null
bool has_field(const rapidjson::Value& obj, const char* key);

// Helper to write optional string field
template<typename Writer>
void write_optional_string(Writer& writer, const char* key, const std::optional<std::string>& value) {
    if (value.has_value()) {
        writer.Key(key);
        writer.String(value->c_str());
    }
}

// Helper to write optional int field
template<typename Writer>
void write_optional_int(Writer& writer, const char* key, const std::optional<int>& value) {
    if (value.has_value()) {
        writer.Key(key);
        writer.Int(*value);
    }
}

// Helper to write optional double field
template<typename Writer>
void write_optional_double(Writer& writer, const char* key, const std::optional<double>& value) {
    if (value.has_value()) {
        writer.Key(key);
        writer.Double(*value);
    }
}

// Helper to write optional bool field
template<typename Writer>
void write_optional_bool(Writer& writer, const char* key, const std::optional<bool>& value) {
    if (value.has_value()) {
        writer.Key(key);
        writer.Bool(*value);
    }
}

} // namespace utils
} // namespace anthropic
