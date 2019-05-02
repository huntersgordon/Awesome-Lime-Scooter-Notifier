
#include <iostream>
#include <string>
#include <array>
#include <fstream>
using namespace std;

std::string exec(const char* cmd) {
    std::array<char, 128> buffer;
    std::string result;
    std::unique_ptr<FILE, decltype(&pclose)> pipe(popen(cmd, "r"), pclose);
    if (!pipe) {
        throw std::runtime_error("popen() failed!");
    }
    while (fgets(buffer.data(), buffer.size(), pipe.get()) != nullptr) {
        result += buffer.data();
    }
    return result;
}

int main(){

string phone;
string loginCode;
cout << "Enter your lime-associated phone number (including country code): ";
cin >> phone;
system(("curl --request GET \
  --url \'https://web-production.lime.bike/api/rider/v1/login?phone=" + phone + "\'").c_str());
cout << "Enter the Lime login code that you were texted:";
cin >> loginCode;
string output = exec(("curl --request POST \
  --cookie-jar - \
  --url \'https://web-production.lime.bike/api/rider/v1/login\' \
  --header \'Content-Type: application/json\' \
  --data \'{\"login_code\": \""+ loginCode + "\", \"phone\": \"+" + phone + "\"}\'").c_str());

ofstream myfile;
myfile.open ("LimeUser.txt");
myfile << output;
myfile.close();
return 0;




}
