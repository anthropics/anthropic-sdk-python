#include "anthropic/http/winhttp_client.hpp"
#include "anthropic/types/errors.hpp"
#include <sstream>
#include <algorithm>

//#pragma comment(lib, "winhttp.lib")

namespace anthropic {
namespace http {

WinHttpClient::WinHttpClient() {
    session_handle_ = WinHttpOpen(
        L"Anthropic-CPP-SDK/1.0",
        WINHTTP_ACCESS_TYPE_DEFAULT_PROXY,
        WINHTTP_NO_PROXY_NAME,
        WINHTTP_NO_PROXY_BYPASS,
        0
    );

    if (!session_handle_) {
        throw ConnectionError("Failed to initialize WinHTTP session");
    }

    // Enable HTTP/2
    DWORD http2 = WINHTTP_PROTOCOL_FLAG_HTTP2;
    WinHttpSetOption(session_handle_, WINHTTP_OPTION_ENABLE_HTTP_PROTOCOL, &http2, sizeof(http2));
}

WinHttpClient::~WinHttpClient() {
    if (session_handle_) {
        WinHttpCloseHandle(session_handle_);
    }
}

std::wstring WinHttpClient::to_wide(const std::string& str) {
    if (str.empty()) return std::wstring();
    int size = MultiByteToWideChar(CP_UTF8, 0, str.c_str(), -1, nullptr, 0);
    std::wstring wstr(size - 1, 0);
    MultiByteToWideChar(CP_UTF8, 0, str.c_str(), -1, &wstr[0], size);
    return wstr;
}

std::string WinHttpClient::to_narrow(const std::wstring& wstr) {
    if (wstr.empty()) return std::string();
    int size = WideCharToMultiByte(CP_UTF8, 0, wstr.c_str(), -1, nullptr, 0, nullptr, nullptr);
    std::string str(size - 1, 0);
    WideCharToMultiByte(CP_UTF8, 0, wstr.c_str(), -1, &str[0], size, nullptr, nullptr);
    return str;
}

WinHttpClient::URLComponents WinHttpClient::parse_url(const std::string& url) {
    std::wstring wurl = to_wide(url);
    URL_COMPONENTS urlComp = {0};
    urlComp.dwStructSize = sizeof(urlComp);

    wchar_t scheme[32] = {0};
    wchar_t host[256] = {0};
    wchar_t path[2048] = {0};

    urlComp.lpszScheme = scheme;
    urlComp.dwSchemeLength = _countof(scheme);
    urlComp.lpszHostName = host;
    urlComp.dwHostNameLength = _countof(host);
    urlComp.lpszUrlPath = path;
    urlComp.dwUrlPathLength = _countof(path);

    if (!WinHttpCrackUrl(wurl.c_str(), 0, 0, &urlComp)) {
        throw BadRequestError("Invalid URL: " + url);
    }

    URLComponents components;
    components.scheme = scheme;
    components.host = host;
    components.port = urlComp.nPort;
    components.path = path;

    return components;
}

HINTERNET WinHttpClient::get_connection(const std::wstring& host, int port) {
    HINTERNET connect = WinHttpConnect(session_handle_, host.c_str(), static_cast<INTERNET_PORT>(port), 0);
    if (!connect) {
        throw ConnectionError("Failed to connect to host");
    }
    return connect;
}

void WinHttpClient::parse_response_headers(HINTERNET request_handle, Response& response) {
    DWORD size = 0;
    WinHttpQueryHeaders(request_handle, WINHTTP_QUERY_RAW_HEADERS_CRLF,
                        WINHTTP_HEADER_NAME_BY_INDEX, nullptr, &size, WINHTTP_NO_HEADER_INDEX);

    if (GetLastError() != ERROR_INSUFFICIENT_BUFFER) return;

    std::vector<wchar_t> buffer(size / sizeof(wchar_t));
    if (WinHttpQueryHeaders(request_handle, WINHTTP_QUERY_RAW_HEADERS_CRLF,
                           WINHTTP_HEADER_NAME_BY_INDEX, buffer.data(), &size, WINHTTP_NO_HEADER_INDEX)) {
        std::wstring headers_str(buffer.data());
        std::wistringstream stream(headers_str);
        std::wstring line;

        while (std::getline(stream, line)) {
            if (line.empty() || line == L"\r") continue;

            size_t colon = line.find(L':');
            if (colon != std::wstring::npos) {
                std::wstring key = line.substr(0, colon);
                std::wstring value = line.substr(colon + 1);

                // Trim whitespace
                value.erase(0, value.find_first_not_of(L" \t\r\n"));
                value.erase(value.find_last_not_of(L" \t\r\n") + 1);

                // Convert to lowercase for key
                std::transform(key.begin(), key.end(), key.begin(), ::towlower);

                response.headers[to_narrow(key)] = to_narrow(value);
            }
        }
    }
}

void WinHttpClient::set_default_headers(const std::map<std::string, std::string>& headers) {
    std::lock_guard<std::mutex> lock(mutex_);
    default_headers_ = headers;
}

Response WinHttpClient::execute(const Request& request) {
    Response response;

    try {
        auto components = parse_url(request.url);
        HINTERNET connect = get_connection(components.host, components.port);

        if (!connect) {
            response.success = false;
            return response;
        }

        DWORD flags = (components.scheme == L"https") ? WINHTTP_FLAG_SECURE : 0;
        std::wstring method = to_wide(request.method);

        HINTERNET request_handle = WinHttpOpenRequest(
            connect,
            method.c_str(),
            components.path.c_str(),
            nullptr,
            WINHTTP_NO_REFERER,
            WINHTTP_DEFAULT_ACCEPT_TYPES,
            flags
        );

        if (!request_handle) {
            WinHttpCloseHandle(connect);
            throw ConnectionError("Failed to create request");
        }

        // Set timeouts
        WinHttpSetTimeouts(request_handle, 60000, 60000, 60000, request.timeout_ms);

        // Build headers
        std::wstring headers_str;
        auto all_headers = default_headers_;
        for (const auto& [key, value] : request.headers) {
            all_headers[key] = value;
        }

        for (const auto& [key, value] : all_headers) {
            headers_str += to_wide(key) + L": " + to_wide(value) + L"\r\n";
        }

        // Send request
        const void* body_ptr = request.body.empty() ? WINHTTP_NO_REQUEST_DATA : request.body.data();
        DWORD body_size = static_cast<DWORD>(request.body.size());

        BOOL result = WinHttpSendRequest(
            request_handle,
            headers_str.c_str(),
            static_cast<DWORD>(-1), // Fix: cast -1 to DWORD to resolve C4245
            const_cast<void*>(body_ptr),
            body_size,
            body_size,
            0
        );

        if (!result) {
            WinHttpCloseHandle(request_handle);
            WinHttpCloseHandle(connect);
            throw ConnectionError("Failed to send request");
        }

        // Receive response
        if (!WinHttpReceiveResponse(request_handle, nullptr)) {
            WinHttpCloseHandle(request_handle);
            WinHttpCloseHandle(connect);
            throw ConnectionError("Failed to receive response");
        }

        // Get status code
        DWORD status_code = 0;
        DWORD size = sizeof(status_code);
        WinHttpQueryHeaders(request_handle, WINHTTP_QUERY_STATUS_CODE | WINHTTP_QUERY_FLAG_NUMBER,
                           WINHTTP_HEADER_NAME_BY_INDEX, &status_code, &size, WINHTTP_NO_HEADER_INDEX);
        response.status_code = status_code;

        // Parse headers
        parse_response_headers(request_handle, response);

        // Read body
        std::string body;
        DWORD bytes_available = 0;
        std::vector<char> buffer(8192);

        while (WinHttpQueryDataAvailable(request_handle, &bytes_available) && bytes_available > 0) {
            DWORD bytes_read = 0;
            DWORD to_read = std::min(bytes_available, static_cast<DWORD>(buffer.size()));

            if (WinHttpReadData(request_handle, buffer.data(), to_read, &bytes_read)) {
                body.append(buffer.data(), bytes_read);
            } else {
                break;
            }
        }

        response.body = body;
        response.success = true;

        WinHttpCloseHandle(request_handle);
        WinHttpCloseHandle(connect);

    } catch (const std::exception&) {
        response.success = false;
        throw;
    }

    return response;
}

Response WinHttpClient::execute_stream(const Request& request, StreamCallback callback) {
    Response response;

    try {
        auto components = parse_url(request.url);
        HINTERNET connect = get_connection(components.host, components.port);

        if (!connect) {
            response.success = false;
            return response;
        }

        DWORD flags = (components.scheme == L"https") ? WINHTTP_FLAG_SECURE : 0;
        std::wstring method = to_wide(request.method);

        HINTERNET request_handle = WinHttpOpenRequest(
            connect,
            method.c_str(),
            components.path.c_str(),
            nullptr,
            WINHTTP_NO_REFERER,
            WINHTTP_DEFAULT_ACCEPT_TYPES,
            flags
        );

        if (!request_handle) {
            WinHttpCloseHandle(connect);
            throw ConnectionError("Failed to create request");
        }

        WinHttpSetTimeouts(request_handle, 60000, 60000, 60000, request.timeout_ms);

        // Build headers
        std::wstring headers_str;
        auto all_headers = default_headers_;
        for (const auto& [key, value] : request.headers) {
            all_headers[key] = value;
        }

        for (const auto& [key, value] : all_headers) {
            headers_str += to_wide(key) + L": " + to_wide(value) + L"\r\n";
        }

        // Send request
        const void* body_ptr = request.body.empty() ? WINHTTP_NO_REQUEST_DATA : request.body.data();
        DWORD body_size = static_cast<DWORD>(request.body.size());

        BOOL result = WinHttpSendRequest(
            request_handle,
            headers_str.c_str(),
            static_cast<DWORD>(-1),
            const_cast<void*>(body_ptr),
            body_size,
            body_size,
            0
        );

        if (!result) {
            WinHttpCloseHandle(request_handle);
            WinHttpCloseHandle(connect);
            throw ConnectionError("Failed to send request");
        }

        if (!WinHttpReceiveResponse(request_handle, nullptr)) {
            WinHttpCloseHandle(request_handle);
            WinHttpCloseHandle(connect);
            throw ConnectionError("Failed to receive response");
        }

        // Get status code
        DWORD status_code = 0;
        DWORD size = sizeof(status_code);
        WinHttpQueryHeaders(request_handle, WINHTTP_QUERY_STATUS_CODE | WINHTTP_QUERY_FLAG_NUMBER,
                           WINHTTP_HEADER_NAME_BY_INDEX, &status_code, &size, WINHTTP_NO_HEADER_INDEX);
        response.status_code = status_code;

        parse_response_headers(request_handle, response);

        // Stream body with callback
        DWORD bytes_available = 0;
        std::vector<char> buffer(8192);
        bool continue_streaming = true;

        while (continue_streaming && WinHttpQueryDataAvailable(request_handle, &bytes_available) && bytes_available > 0) {
            DWORD bytes_read = 0;
            DWORD to_read = std::min(bytes_available, static_cast<DWORD>(buffer.size()));

            if (WinHttpReadData(request_handle, buffer.data(), to_read, &bytes_read)) {
                std::string chunk(buffer.data(), bytes_read);
                continue_streaming = callback(chunk);
            } else {
                break;
            }
        }

        response.success = true;

        WinHttpCloseHandle(request_handle);
        WinHttpCloseHandle(connect);

    } catch (const std::exception&) {
        response.success = false;
        throw;
    }

    return response;
}

std::unique_ptr<HttpClient> create_http_client() {
    return std::make_unique<WinHttpClient>();
}

} // namespace http
} // namespace anthropic
