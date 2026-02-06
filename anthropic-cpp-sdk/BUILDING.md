# Building the Anthropic C++ SDK

This guide provides detailed instructions for building the Anthropic C++ SDK on Windows.

## Prerequisites

### Required Software

1. **Visual Studio 2022** (or later)
   - Community, Professional, or Enterprise edition
   - Install "Desktop development with C++" workload
   - Ensure C++20 support is installed

2. **Windows SDK**
   - Usually included with Visual Studio
   - Provides WinHTTP and other system libraries
   - Version 10.0 or later

### Verifying Prerequisites

Open Developer Command Prompt for VS 2022 and run:

```cmd
cl /version
```

Should show: `Microsoft (R) C/C++ Optimizing Compiler Version 19.xx or later`

## Build Steps

### Option 1: Visual Studio IDE

1. **Open Solution**
   ```
   Double-click AnthropicSDK.sln
   ```

2. **Select Configuration**
   - Use dropdown at top: `Debug` or `Release`
   - Platform: `x64` (only x64 is supported)

3. **Build**
   - Menu: Build → Build Solution
   - Or press: `Ctrl+Shift+B`
   - Or right-click project → Build

4. **Output Location**
   - Debug: `bin\x64\Debug\AnthropicSDK.lib`
   - Release: `bin\x64\Release\AnthropicSDK.lib`

### Option 2: MSBuild Command Line

Open "Developer Command Prompt for VS 2022" in the project directory:

**Debug Build:**
```cmd
msbuild AnthropicSDK.sln /p:Configuration=Debug /p:Platform=x64
```

**Release Build:**
```cmd
msbuild AnthropicSDK.sln /p:Configuration=Release /p:Platform=x64
```

**Clean Build:**
```cmd
msbuild AnthropicSDK.sln /t:Clean /p:Configuration=Release /p:Platform=x64
msbuild AnthropicSDK.sln /p:Configuration=Release /p:Platform=x64
```

## Build Configurations

### Debug Configuration

- Optimization: Disabled
- Runtime Library: Multi-threaded Debug (`/MTd`)
- Debug Information: Full
- Preprocessor: `_DEBUG`
- Use for: Development and debugging

### Release Configuration

- Optimization: Full (`/O2`, `/Oi`)
- Runtime Library: Multi-threaded (`/MT`)
- Debug Information: PDB file for debugging
- Preprocessor: `NDEBUG`
- Link-Time Code Generation: Enabled
- Use for: Production builds

## Using the Library

### In Your Visual Studio Project

1. **Add Include Directory**
   ```
   Project → Properties → C/C++ → General → Additional Include Directories
   Add: C:\SOURCES\anthropic-sdk\anthropic-cpp-sdk\include
   Add: C:\SOURCES\anthropic-sdk\anthropic-cpp-sdk\third_party
   ```

2. **Add Library Directory**
   ```
   Project → Properties → Linker → General → Additional Library Directories
   Add: C:\SOURCES\anthropic-sdk\anthropic-cpp-sdk\bin\x64\$(Configuration)
   ```

3. **Add Library Dependencies**
   ```
   Project → Properties → Linker → Input → Additional Dependencies
   Add: AnthropicSDK.lib;winhttp.lib;ws2_32.lib;crypt32.lib
   ```

4. **Set Language Standard**
   ```
   Project → Properties → C/C++ → Language → C++ Language Standard
   Set to: ISO C++20 Standard (/std:c++20)
   ```

5. **Match Runtime Library**
   ```
   Project → Properties → C/C++ → Code Generation → Runtime Library
   Debug: Multi-threaded Debug (/MTd)
   Release: Multi-threaded (/MT)

   IMPORTANT: Must match the SDK build configuration!
   ```

### Example Project Setup

Create `example.cpp`:

```cpp
#include <anthropic/client.hpp>
#include <anthropic/resources/messages.hpp>
#include <iostream>

int main() {
    try {
        anthropic::Client client;

        anthropic::resources::MessageCreateParams params;
        params.model = "claude-sonnet-4-5-20250929";
        params.max_tokens = 100;

        anthropic::resources::types::MessageParam msg;
        msg.role = "user";
        msg.content = "Hello!";
        params.messages.push_back(msg);

        auto response = client.messages().create(params);
        std::cout << "Success!" << std::endl;

    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
    return 0;
}
```

Compile:

```cmd
cl /EHsc /std:c++20 /MD /I"C:\SOURCES\anthropic-sdk\anthropic-cpp-sdk\include" /I"C:\SOURCES\anthropic-sdk\anthropic-cpp-sdk\third_party" example.cpp /link AnthropicSDK.lib winhttp.lib ws2_32.lib crypt32.lib /LIBPATH:"C:\SOURCES\anthropic-sdk\anthropic-cpp-sdk\bin\x64\Release"
```

## Troubleshooting

### Common Build Errors

**Error: Cannot open include file 'rapidjson/document.h'**
- Solution: Verify `third_party/rapidjson` directory exists
- Download RapidJSON if missing: https://github.com/Tencent/rapidjson
- Copy `include/rapidjson` to `third_party/rapidjson`

**Error: LNK2019 unresolved external symbol**
- Solution: Add missing library dependencies:
  - `winhttp.lib` - HTTP client
  - `ws2_32.lib` - Windows Sockets
  - `crypt32.lib` - Cryptography

**Error: Runtime Library Mismatch**
```
LINK : warning LNK4098: defaultlib 'LIBCMT' conflicts with use of other libs
```
- Solution: Ensure your project uses the same runtime library as the SDK
- SDK uses `/MT` (Release) or `/MTd` (Debug)
- Check: Project → Properties → C/C++ → Code Generation → Runtime Library

**Error: 'std::optional' not found**
- Solution: Set C++ Language Standard to C++20
- Project → Properties → C/C++ → Language → C++ Language Standard: `/std:c++20`

**Error: Cannot find 'winhttp.h'**
- Solution: Install Windows SDK via Visual Studio Installer
- Open Visual Studio Installer → Modify → Individual Components
- Select "Windows 10 SDK" or later

### Debug Tips

**Enable Verbose Build Output:**
```
Tools → Options → Projects and Solutions → Build and Run
Set "MSBuild project build output verbosity" to "Detailed"
```

**Check Library Path:**
```cmd
dumpbin /exports bin\x64\Release\AnthropicSDK.lib
```

**Verify Dependencies:**
```cmd
dumpbin /dependents your_executable.exe
```

## Build Performance

### Optimization Tips

1. **Use Release Build for Production**
   - Debug builds are 3-5x slower
   - Release uses full optimization

2. **Enable Multi-Processor Compilation**
   ```
   Project → Properties → C/C++ → General → Multi-processor Compilation: Yes (/MP)
   ```

3. **Use Precompiled Headers** (if adding many files)
   ```
   Project → Properties → C/C++ → Precompiled Headers
   ```

4. **Incremental Linking** (Debug only)
   - Already enabled by default
   - Speeds up repeated builds

### Build Times

Approximate build times on modern hardware:

- Clean Debug Build: 10-15 seconds
- Clean Release Build: 15-20 seconds
- Incremental Build: 2-5 seconds

## Advanced Configuration

### Custom Include Paths

If you need to use the SDK from a different location:

1. **Environment Variable Method**
   ```cmd
   set ANTHROPIC_SDK_ROOT=C:\path\to\anthropic-cpp-sdk
   ```

2. **Update Project Properties**
   ```
   Additional Include Directories: $(ANTHROPIC_SDK_ROOT)\include;$(ANTHROPIC_SDK_ROOT)\third_party
   Additional Library Directories: $(ANTHROPIC_SDK_ROOT)\bin\x64\$(Configuration)
   ```

### Static vs Dynamic Runtime

The SDK is configured for static runtime (`/MT`) to minimize dependencies.

To use dynamic runtime (`/MD`):

1. Change SDK project settings:
   ```
   Project → Properties → C/C++ → Code Generation → Runtime Library
   Release: /MD
   Debug: /MDd
   ```

2. Rebuild the SDK

3. Update your project to match

**Note:** All libraries in your project must use the same runtime!

### Custom Build Macros

Add custom defines in project properties:

```
Project → Properties → C/C++ → Preprocessor → Preprocessor Definitions
```

Useful defines:
- `ANTHROPIC_DEBUG_HTTP` - Enable HTTP request/response logging
- `ANTHROPIC_NO_RETRY` - Disable automatic retry
- `ANTHROPIC_CUSTOM_BASE_URL` - Override default API URL

## Distribution

### Packaging for Distribution

When distributing your application:

1. **Include Libraries**
   - `AnthropicSDK.lib` (static library)
   - No DLLs required (statically linked)

2. **Include Headers** (if distributing as SDK)
   - Copy `include/anthropic/` directory
   - Copy `third_party/rapidjson/` directory

3. **Redistribution Requirements**
   - No Visual C++ Redistributable needed (static linking)
   - Requires Windows 10 or later

### Creating a NuGet Package (Optional)

```cmd
nuget pack AnthropicSDK.nuspec
```

Example `AnthropicSDK.nuspec`:

```xml
<?xml version="1.0"?>
<package>
  <metadata>
    <id>AnthropicSDK</id>
    <version>0.1.0</version>
    <authors>Your Name</authors>
    <description>C++ SDK for Anthropic Claude API</description>
    <requireLicenseAcceptance>false</requireLicenseAcceptance>
  </metadata>
  <files>
    <file src="bin\x64\Release\AnthropicSDK.lib" target="lib\x64\Release" />
    <file src="bin\x64\Debug\AnthropicSDK.lib" target="lib\x64\Debug" />
    <file src="include\**\*" target="include" />
  </files>
</package>
```

## Testing the Build

### Quick Test

```cmd
cd examples
cl /EHsc /std:c++20 /MT /I..\include /I..\third_party basic_message.cpp /link ..\bin\x64\Release\AnthropicSDK.lib winhttp.lib ws2_32.lib crypt32.lib

set ANTHROPIC_API_KEY=your-api-key-here
basic_message.exe
```

### Verify Static Linking

Check that the executable has no unexpected DLL dependencies:

```cmd
dumpbin /dependents basic_message.exe
```

Should only show system DLLs:
- `KERNEL32.dll`
- `USER32.dll`
- `WINHTTP.dll`
- etc.

No Visual C++ runtime DLLs should be listed.

## Getting Help

If you encounter build issues:

1. Check this guide for common solutions
2. Verify all prerequisites are installed
3. Try a clean rebuild
4. Check Visual Studio output window for detailed errors
5. Open an issue on GitHub with:
   - Visual Studio version
   - Windows version
   - Full build error output
   - Steps to reproduce
