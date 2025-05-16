//===============Python Command========================================
#include <iostream>
#include <windows.h>
#include <string>

using namespace std;

// DLL function pointer types
typedef void(__stdcall* InitializeFunc)(long, long);
typedef void(__stdcall* IEsendFunc)(long, const char*, long, long&);
typedef void(__stdcall* IEenterFunc)(char*, long, long&, long, long&);
typedef long(__stdcall* GpibBoardPresentFunc)();
typedef long(__stdcall* ListenerPresentFunc)(long);

// Send GPIB command
void send(IEsendFunc IEsend, int addr, const string& cmd, long& status) {
    IEsend(addr, cmd.c_str(), -1, status);
}

// Read GPIB response
string enter(IEenterFunc IEenter, int addr, long maxlen, long& status) {
    char* buffer = new char[maxlen + 1];
    long receivedLen = 0;
    IEenter(buffer, maxlen, receivedLen, addr, status);
    buffer[receivedLen] = '\0';
    string result(buffer);
    delete[] buffer;
    return result;
}

// Parse "Cap,DF" string
pair<string, string> parseCapDf(const string& data) {
    size_t commaPos = data.find(',');
    if (commaPos != string::npos) {
        return {
            data.substr(0, commaPos),
            data.substr(commaPos + 1)
        };
    }
    return { data, "" };
}

int main() {
    const int deviceAddr = 17;
    long status = 0;
    int boardAddr = -1;

    // Load DLL
    HINSTANCE hDLL = LoadLibraryA("IEEE_32M.DLL");
    if (!hDLL) {
        cerr << "Failed to load IEEE_32M.DLL" << endl;
        return 1;
    }

    // Load functions
    InitializeFunc initialize = (InitializeFunc)GetProcAddress(hDLL, "_ieee_initialize@8");
    IEsendFunc IEsend = (IEsendFunc)GetProcAddress(hDLL, "_ieee_send@16");
    IEenterFunc IEenter = (IEenterFunc)GetProcAddress(hDLL, "_ieee_enter@20");
    GpibBoardPresentFunc GpibBoardPresent = (GpibBoardPresentFunc)GetProcAddress(hDLL, "_ieee_board_present@0");
    ListenerPresentFunc ListenerPresent = (ListenerPresentFunc)GetProcAddress(hDLL, "_ieee_listener_present@4");

    if (!initialize || !IEsend || !IEenter || !GpibBoardPresent || !ListenerPresent) {
        cerr << "Failed to load one or more functions from the DLL." << endl;
        FreeLibrary(hDLL);
        return 1;
    }

    // Check board presence
    if (!GpibBoardPresent()) {
        cerr << "No GPIB-compatible board detected." << endl;
        FreeLibrary(hDLL);
        return 1;
    }

    // Try possible board addresses
    for (int addrTry : {21, 0}) {
        initialize(addrTry, 0);
        if (ListenerPresent(deviceAddr)) {
            boardAddr = addrTry;
            break;
        }
    }

    if (boardAddr == -1) {
        cerr << "Could not detect HP4278A on GPIB or USB-488." << endl;
        FreeLibrary(hDLL);
        return 1;
    }

    // Trigger new measurement via GPIB
    send(IEsend, deviceAddr, "TRIG2", status);
    send(IEsend, deviceAddr, "*TRG", status);
    Sleep(300);  // wait for measurement to settle

    // Request data
    send(IEsend, deviceAddr, "DATA?", status);
    string response = enter(IEenter, deviceAddr, 80, status);

    pair<string, string> capData = parseCapDf(response);
    string CapStr = capData.first;
    string DfStr = capData.second;

    cout << "Capacitance: " << CapStr << " pF" << endl;
    cout << "Dissipation Factor: " << DfStr << endl;

    FreeLibrary(hDLL);
    return 0;
}






//_____________________________________________________________________________________________
//#include <iostream>
//#include <windows.h>
//#include <string>
//
//using namespace std;
//
//// DLL function pointer types
//typedef void(__stdcall* InitializeFunc)(long, long);
//typedef void(__stdcall* IEsendFunc)(long, const char*, long, long&);
//typedef void(__stdcall* IEenterFunc)(char*, long, long&, long, long&);
//typedef long(__stdcall* GpibBoardPresentFunc)();
//typedef long(__stdcall* ListenerPresentFunc)(long);
//
//// Send GPIB command
//void send(IEsendFunc IEsend, int addr, const string& cmd, long& status) {
//    IEsend(addr, cmd.c_str(), -1, status);
//}
//
//// Read GPIB response
//string enter(IEenterFunc IEenter, int addr, long maxlen, long& status) {
//    char* buffer = new char[maxlen + 1];
//    long receivedLen = 0;
//    IEenter(buffer, maxlen, receivedLen, addr, status);
//    buffer[receivedLen] = '\0';
//    string result(buffer);
//    delete[] buffer;
//    return result;
//}
//
//// Parse "Cap,DF" string
//pair<string, string> parseCapDf(const string& data) {
//    size_t commaPos = data.find(',');
//    if (commaPos != string::npos) {
//        return {
//            data.substr(0, commaPos),
//            data.substr(commaPos + 1)
//        };
//    }
//    return { data, "" };
//}
//
//int main() {
//    const int deviceAddr = 17;
//    long status = 0;
//    int boardAddr = -1;
//
//    // Load DLL
//    HINSTANCE hDLL = LoadLibraryA("IEEE_32M.DLL");
//    if (!hDLL) {
//        cerr << "Failed to load IEEE_32M.DLL" << endl;
//        return 1;
//    }
//
//    // Load functions
//    InitializeFunc initialize = (InitializeFunc)GetProcAddress(hDLL, "_ieee_initialize@8");
//    IEsendFunc IEsend = (IEsendFunc)GetProcAddress(hDLL, "_ieee_send@16");
//    IEenterFunc IEenter = (IEenterFunc)GetProcAddress(hDLL, "_ieee_enter@20");
//    GpibBoardPresentFunc GpibBoardPresent = (GpibBoardPresentFunc)GetProcAddress(hDLL, "_ieee_board_present@0");
//    ListenerPresentFunc ListenerPresent = (ListenerPresentFunc)GetProcAddress(hDLL, "_ieee_listener_present@4");
//
//    if (!initialize || !IEsend || !IEenter || !GpibBoardPresent || !ListenerPresent) {
//        cerr << "Failed to load one or more functions from the DLL." << endl;
//        FreeLibrary(hDLL);
//        return 1;
//    }
//
//    // Check board presence
//    if (!GpibBoardPresent()) {
//        cerr << "No GPIB-compatible board detected." << endl;
//        FreeLibrary(hDLL);
//        return 1;
//    }
//
//    // Try possible board addresses
//    for (int addrTry : {21, 0}) {
//        initialize(addrTry, 0);
//        if (ListenerPresent(deviceAddr)) {
//            boardAddr = addrTry;
//            cout << "Connection successful via board address " << boardAddr << endl;
//            break;
//        }
//    }
//
//    if (boardAddr == -1) {
//        cerr << "Could not detect HP4278A on GPIB or USB-488." << endl;
//        FreeLibrary(hDLL);
//        return 1;
//    }
//
//    // Loop for multiple readings
//    while (true) {
//        cout << "\nPress ENTER to trigger a new reading, or type '1' then ENTER to quit: ";
//        string userInput;
//        getline(cin, userInput);
//
//        if (userInput == "1") {
//            break;
//        }
//
//        // Trigger new measurement via GPIB
//        send(IEsend, deviceAddr, "TRIG2", status);
//        send(IEsend, deviceAddr, "*TRG", status);
//        Sleep(300);  // wait for measurement to settle
//
//        // Request data
//        send(IEsend, deviceAddr, "DATA?", status);
//        string response = enter(IEenter, deviceAddr, 80, status);
//
//        pair<string, string> capData = parseCapDf(response);
//        string CapStr = capData.first;
//        string DfStr = capData.second;
//
//        cout << "Capacitance: " << CapStr << " pF" << endl;
//        cout << "Dissipation Factor: " << DfStr << endl;
//    }
//
//    cout << "Exiting..." << endl;
//    FreeLibrary(hDLL);
//    return 0;
//}




//#include <iostream>
//#include <windows.h>
//#include <string>
//
//using namespace std;
//
//// DLL function pointer types
//typedef void(__stdcall* InitializeFunc)(long, long);
//typedef void(__stdcall* IEsendFunc)(long, const char*, long, long&);
//typedef void(__stdcall* IEenterFunc)(char*, long, long&, long, long&);
//typedef long(__stdcall* GpibBoardPresentFunc)();
//typedef long(__stdcall* ListenerPresentFunc)(long);
//
//// Send GPIB command
//void send(IEsendFunc IEsend, int addr, const string& cmd, long& status) {
//    IEsend(addr, cmd.c_str(), -1, status);
//}
//
//// Read GPIB response
//string enter(IEenterFunc IEenter, int addr, long maxlen, long& status) {
//    char* buffer = new char[maxlen + 1];
//    long receivedLen = 0;
//    IEenter(buffer, maxlen, receivedLen, addr, status);
//    buffer[receivedLen] = '\0';
//    string result(buffer);
//    delete[] buffer;
//    return result;
//}
//
//// Parse "Cap,DF" string
//pair<string, string> parseCapDf(const string& data) {
//    size_t commaPos = data.find(',');
//    if (commaPos != string::npos) {
//        return {
//            data.substr(0, commaPos),
//            data.substr(commaPos + 1)
//        };
//    }
//    return { data, "" };
//}
//
//int main() {
//    const int boardAddr = 21;
//    const int deviceAddr = 17;
//    long status = 0;
//
//    // Load DLL
//    HINSTANCE hDLL = LoadLibraryA("IEEE_32M.DLL");
//    if (!hDLL) {
//        cerr << "Failed to load IEEE_32M.DLL" << endl;
//        return 1;
//    }
//
//    // Load functions
//    InitializeFunc initialize = (InitializeFunc)GetProcAddress(hDLL, "_ieee_initialize@8");
//    IEsendFunc IEsend = (IEsendFunc)GetProcAddress(hDLL, "_ieee_send@16");
//    IEenterFunc IEenter = (IEenterFunc)GetProcAddress(hDLL, "_ieee_enter@20");
//    GpibBoardPresentFunc GpibBoardPresent = (GpibBoardPresentFunc)GetProcAddress(hDLL, "_ieee_board_present@0");
//    ListenerPresentFunc ListenerPresent = (ListenerPresentFunc)GetProcAddress(hDLL, "_ieee_listener_present@4");
//
//    if (!initialize || !IEsend || !IEenter || !GpibBoardPresent || !ListenerPresent) {
//        cerr << "Failed to load one or more functions from the DLL." << endl;
//        FreeLibrary(hDLL);
//        return 1;
//    }
//
//    // Check board
//    if (!GpibBoardPresent()) {
//        cerr << "GPIB board not present." << endl;
//        FreeLibrary(hDLL);
//        return 1;
//    }
//
//    // Init board
//    initialize(boardAddr, 0);
//
//    // Check instrument
//    if (ListenerPresent(deviceAddr) == 0) {
//        cerr << "HP4278A not found." << endl;
//        FreeLibrary(hDLL);
//        return 1;
//    }
//
//    // Loop for multiple readings
//    while (true) {
//        cout << "\nPress ENTER to trigger a new reading, or type '1' then ENTER to quit: ";
//        string userInput;
//        getline(cin, userInput);
//       
//        if (userInput == "1") {
//            break;
//        }
//
//        // Trigger new measurement via GPIB
//        send(IEsend, deviceAddr, "TRIG2", status);
//        send(IEsend, deviceAddr, "*TRG", status);
//        Sleep(300);  // wait for measurement to settle
//
//        // Request data
//        send(IEsend, deviceAddr, "DATA?", status);
//        string response = enter(IEenter, deviceAddr, 80, status);
//
//        pair<string, string> capData = parseCapDf(response);
//        string CapStr = capData.first;
//        string DfStr = capData.second;
//
//        cout << "Capacitance: " << CapStr << " pF" << endl;
//        cout << "Dissipation Factor: " << DfStr << endl;
//    }
//
//    cout << "Exiting..." << endl;
//    FreeLibrary(hDLL);
//    return 0;
//}







//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//#include <iostream>
//#include <windows.h>
//#include <string>
//
//using namespace std;
//
//// Define function pointer types that match the DLL exports
//typedef void(__stdcall* InitializeFunc)(long, long);
//typedef void(__stdcall* IEsendFunc)(long, const char*, long, long&);
//typedef void(__stdcall* IEenterFunc)(char*, long, long&, long, long&);
//typedef long(__stdcall* GpibBoardPresentFunc)();
//typedef long(__stdcall* ListenerPresentFunc)(long);
//
//// Send GPIB command
//void send(IEsendFunc IEsend, int addr, const string& cmd, long& status) {
//    IEsend(addr, cmd.c_str(), -1, status);
//}
//
//// Read GPIB response
//string enter(IEenterFunc IEenter, int addr, long maxlen, long& status) {
//    char* buffer = new char[maxlen + 1];
//    long receivedLen = 0;
//    IEenter(buffer, maxlen, receivedLen, addr, status);
//    buffer[receivedLen] = '\0';
//    string result(buffer);
//    delete[] buffer;
//    return result;
//}
//
//// Parse "Cap,DF" string into pair
//pair<string, string> parseCapDf(const string& data) {
//    size_t commaPos = data.find(',');
//    if (commaPos != string::npos) {
//        return {
//            data.substr(0, commaPos),
//            data.substr(commaPos + 1)
//        };
//    }
//    return { data, "" };
//}
//
//int main() {
//    const int boardAddr = 21;
//    const int deviceAddr = 17;
//    long status = 0;
//
//    // Load the DLL
//    HINSTANCE hDLL = LoadLibraryA("IEEE_32M.DLL");
//    if (!hDLL) {
//        cerr << "❌ Failed to load IEEE_32M.DLL" << endl;
//        return 1;
//    }
//
//    // Load functions
//    InitializeFunc initialize = (InitializeFunc)GetProcAddress(hDLL, "_ieee_initialize@8");
//    IEsendFunc IEsend = (IEsendFunc)GetProcAddress(hDLL, "_ieee_send@16");
//    IEenterFunc IEenter = (IEenterFunc)GetProcAddress(hDLL, "_ieee_enter@20");
//    GpibBoardPresentFunc GpibBoardPresent = (GpibBoardPresentFunc)GetProcAddress(hDLL, "_ieee_board_present@0");
//    ListenerPresentFunc ListenerPresent = (ListenerPresentFunc)GetProcAddress(hDLL, "_ieee_listener_present@4");
//
//    // Check for missing functions
//    if (!initialize || !IEsend || !IEenter || !GpibBoardPresent || !ListenerPresent) {
//        cerr << "❌ One or more functions could not be loaded from the DLL." << endl;
//        FreeLibrary(hDLL);
//        return 1;
//    }
//
//    // Step 1: Check board presence
//    if (!GpibBoardPresent()) {
//        cerr << "❌ GPIB board not present." << endl;
//        FreeLibrary(hDLL);
//        return 1;
//    }
//
//    // Step 2: Initialize board
//    initialize(boardAddr, 0);
//
//    // Step 3: Check for instrument
//    if (ListenerPresent(deviceAddr) == 0) {
//        cerr << "❌ HP4278A not found. Check cable and power." << endl;
//        FreeLibrary(hDLL);
//        return 1;
//    }
//
//    // Step 4: Trigger measurements
//    send(IEsend, deviceAddr, "TRIG2", status);
//    send(IEsend, deviceAddr, "*TRG", status);
//
//    Sleep(300); // Simulate delay
//
//    // Step 5: Request and read data
//    send(IEsend, deviceAddr, "DATA?", status);
//    string response = enter(IEenter, deviceAddr, 80, status);
//
//    // Step 6: Parse and print
//    pair<string, string> capData = parseCapDf(response);
//    string CapStr = capData.first;
//    string DfStr = capData.second;
//
//    cout << "📟 Capacitance: " << CapStr << " pF" << endl;
//    cout << "📟 Dissipation Factor: " << DfStr << endl;
//
//    // Cleanup
//    FreeLibrary(hDLL);
//    return 0;
//}
