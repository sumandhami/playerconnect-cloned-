import 'package:flutter/material.dart';
import 'package:playerconnect/src/common_widgets/Validations/emailvalidation.dart';
import 'package:playerconnect/src/common_widgets/Validations/passwordvalidation.dart';
import 'package:playerconnect/src/features/authentication/screens/forgotpass/forgotpass.dart';
import 'package:playerconnect/src/features/authentication/screens/singup/signup_page.dart';
import 'package:playerconnect/src/pages/home_page.dart';
import '../../../shared_preferences/shared_prefs.dart';

class Loginpage extends StatefulWidget {
  const Loginpage({super.key});

  @override
  _LoginpageState createState() => _LoginpageState();
}

class _LoginpageState extends State<Loginpage> {
  final _formkey = GlobalKey<FormState>(); // Assign this to Form widget
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  Future<void> checkLogin() async {
    Map<String, String?> userData = await SharedPrefs.getUserData();

    if (_emailController.text == userData["email"] &&
        _passwordController.text == userData["password"]) {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (context) => My_HomePage()),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Invalid Email or Password")),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        body: Stack(
          children: [
            // Gradient background
            Container(
              width: double.infinity,
              height: double.infinity,
              decoration: const BoxDecoration(
                gradient: RadialGradient(
                  center: Alignment.center,
                  radius: 0.9,
                  colors: [
                    Color(0xFF1B2A41),
                    Color(0xFF23395B),
                    Color(0xFF2D4A69),
                  ],
                  stops: [0.3, 0.7, 1.0],
                ),
              ),
            ),
            Center(
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 30.0),
                child: SingleChildScrollView(
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      const SizedBox(height: 20),
                      // Text with border
                      Stack(
                        children: [
                          Text(
                            "FUTSAL PLAYER CONNECT",
                            style: TextStyle(
                              fontFamily: 'Kanit',
                              fontSize: 28,
                              fontWeight: FontWeight.bold,
                              letterSpacing: 2,
                              foreground: Paint()
                                ..style = PaintingStyle.stroke
                                ..strokeWidth = 4
                                ..color = Colors.black,
                            ),
                            textAlign: TextAlign.center,
                          ),
                          const Text(
                            "FUTSAL PLAYER CONNECT",
                            style: TextStyle(
                              fontFamily: 'Kanit',
                              fontSize: 28,
                              fontWeight: FontWeight.bold,
                              letterSpacing: 2,
                              color: Colors.white,
                            ),
                            textAlign: TextAlign.center,
                          ),
                        ],
                      ),
                      const SizedBox(height: 8),
                      const Text(
                        "Login to your account",
                        style: TextStyle(
                          fontFamily: 'Kanit',
                          fontSize: 17,
                          fontStyle: FontStyle.italic,
                          color: Colors.white,
                        ),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: 50),

                      // **WRAPPING INPUTS INSIDE FORM**
                      Form(
                        key: _formkey,
                        child: Column(
                          children: [
                            // Email Input
                            Emailvalidation(
                              emailController: _emailController,
                              labelText: "Email",
                            ),
                            const SizedBox(height: 20),

                            // Password Input
                            PasswordValidation(
                              controller: _passwordController,
                              labelText: "Password",
                            ),
                          ],
                        ),
                      ),

                      const SizedBox(height: 30),

                      // **LOGIN BUTTON WITH VALIDATION**
                      ElevatedButton(
                        style: ElevatedButton.styleFrom(
                          backgroundColor: const Color(0xFF65A3B8),
                          foregroundColor: Colors.white,
                          padding: const EdgeInsets.symmetric(
                              horizontal: 50, vertical: 15),
                          side: const BorderSide(color: Colors.white, width: 2),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(8),
                          ),
                          shadowColor: Colors.black,
                          elevation: 10,
                        ),
                        onPressed: () {
                          if (_formkey.currentState!.validate()) {
                            // Navigate only if the form is valid
                            checkLogin();
                          }
                        },
                        child: const Text(
                          "LOGIN",
                          style: TextStyle(
                            fontFamily: 'Kanit',
                            fontSize: 18,
                            fontWeight: FontWeight.w600,
                            letterSpacing: 1,
                          ),
                        ),
                      ),

                      const SizedBox(height: 20),

                      // Forgot Password
                      TextButton(
                        onPressed: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) => Forgotpass(),
                            ),
                          );
                        },
                        child: const Text(
                          "Forgot Password?",
                          style: TextStyle(color: Colors.white),
                        ),
                      ),

                      const SizedBox(height: 20),

                      // Sign Up Link
                      TextButton(
                        onPressed: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) => SignUpPage(),
                            ),
                          );
                        },
                        child: const Text(
                          "Don't have an account? Sign Up",
                          style: TextStyle(color: Colors.white),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
