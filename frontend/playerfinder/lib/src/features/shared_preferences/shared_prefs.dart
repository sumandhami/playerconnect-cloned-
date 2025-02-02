import 'package:shared_preferences/shared_preferences.dart';

class SharedPrefs {
  static Future<void> saveUserData(
    String name,
    String email,
    String phoneno,
    String location,
    String password, {
    String? profilePicture,
  }) async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    await prefs.setString('user_name', name);
    await prefs.setString('email', email);
    await prefs.setString('phone_no', phoneno);
    await prefs.setString('location', location);
    await prefs.setString('password', password);
    if (profilePicture != null) {
      await prefs.setString('profile_picture', profilePicture);
    }
  }

  static Future<Map<String, String?>> getUserData() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    return {
      "name": prefs.getString('user_name'),
      "email": prefs.getString('email'),
      "phone_no": prefs.getString('phone_no'),
      "location": prefs.getString('location'),
      "password": prefs.getString('password'),
      "profile_picture": prefs.getString('profile_picture'),
    };
  }

  static Future<void> clearUserData() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    await prefs.clear();
  }

  // Save online status
  static Future<void> saveOnlineStatus(bool isOnline) async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    await prefs.setBool('is_online', isOnline);
  }

  // Get online status
  static Future<bool> getOnlineStatus() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    return prefs.getBool('is_online') ?? false; // Default to offline if not set
  }
}
