#pragma once

#include "http_client.hpp"
#include <windows.h>
#include <winhttp.h>
#include <mutex>
#include <memory>

namespace anthropic {
namespace http {

class WinHttpClient : public HttpClient {
public:
    WinHttpClient();
    ~WinHttpClient() override;

    Response execute(const Request& request) override;
    Response execute_stream(const Request& request, StreamCallback callback) override;
    void set_default_headers(const std::map<std::string, std::string>& headers) override;

private:
    struct URLComponents {
        std::wstring scheme;
        std::wstring host;
        int port = 0;
        std::wstring path;
    };

    URLComponents parse_url(const std::string& url);
    std::wstring to_wide(const std::string& str);
    std::string to_narrow(const std::wstring& wstr);

    HINTERNET get_connection(const std::wstring& host, int port);
    void parse_response_headers(HINTERNET request_handle, Response& response);

    HINTERNET session_handle_;
    std::map<std::string, std::string> default_headers_;
    std::mutex mutex_;
};

} // namespace http
} // namespace anthropic
