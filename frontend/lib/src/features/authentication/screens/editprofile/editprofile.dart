import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:io';
import '../../../shared_preferences/shared_prefs.dart';

class EditProfilePage extends StatefulWidget {
  const EditProfilePage({super.key});

  @override
  _EditProfilePageState createState() => _EditProfilePageState();
}

class _EditProfilePageState extends State<EditProfilePage> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _emailController = TextEditingController();
  final _phoneController = TextEditingController();
  final _locationController = TextEditingController();
  File? _profileImage; // To store the selected image file

  @override
  void initState() {
    super.initState();
    _loadUserData();
  }

  Future<void> _loadUserData() async {
    Map<String, String?> userData = await SharedPrefs.getUserData();
    setState(() {
      _nameController.text = userData['name'] ?? '';
      _emailController.text = userData['email'] ?? '';
      _phoneController.text = userData['phone_no'] ?? '';
      _locationController.text = userData['location'] ?? '';
      // Load profile picture if saved
      if (userData['profile_picture'] != null) {
        _profileImage = File(userData['profile_picture']!);
      }
    });
  }

  Future<void> _updateProfile() async {
    if (_formKey.currentState!.validate()) {
      await SharedPrefs.saveUserData(
        _nameController.text,
        _emailController.text,
        _phoneController.text,
        _locationController.text,
        '', // Password can be handled separately
        profilePicture: _profileImage?.path, // Save profile picture path
      );
      Navigator.pop(context); // Go back to the homepage
    }
  }

  Future<void> _pickImage() async {
    final picker = ImagePicker();
    final pickedFile = await picker.pickImage(source: ImageSource.gallery);

    if (pickedFile != null) {
      setState(() {
        _profileImage = File(pickedFile.path);
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          'Edit Profile',
          style: TextStyle(
            fontFamily: 'Kanit',
            fontSize: 24,
            fontWeight: FontWeight.bold,
            color: Colors.white,
          ),
        ),
        backgroundColor: Color(0xFF1B2A41),
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            onPressed: _updateProfile,
            icon: Icon(Icons.save, color: Colors.white),
          ),
        ],
      ),
      body: Stack(
        children: [
          // Gradient background
          Container(
            width: double.infinity,
            height: double.infinity,
            decoration: BoxDecoration(
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

          // Content
          SingleChildScrollView(
            padding: const EdgeInsets.all(16.0),
            child: Form(
              key: _formKey,
              child: Column(
                children: [
                  // Profile Card
                  Container(
                    width: double.infinity,
                    padding: const EdgeInsets.all(18.0),
                    decoration: BoxDecoration(
                      gradient: RadialGradient(
                        center: Alignment.center,
                        radius: 0.8,
                        colors: [
                          Color(0xFF23395B),
                          Color(0xFF2D4A69),
                        ],
                        stops: [0.3, 1.0],
                      ),
                      borderRadius: BorderRadius.circular(8),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black.withOpacity(0.3),
                          blurRadius: 15,
                          spreadRadius: 3,
                          offset: const Offset(0, 6),
                        ),
                      ],
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        // Profile Picture with Edit Button
                        Center(
                          child: GestureDetector(
                            onTap: _pickImage, // Open image picker on tap
                            child: Stack(
                              children: [
                                CircleAvatar(
                                  radius: 50,
                                  backgroundImage: _profileImage != null
                                      ? FileImage(_profileImage!)
                                      : AssetImage(
                                              'assets/images/futsaluser.jpeg')
                                          as ImageProvider,
                                ),
                                Positioned(
                                  bottom: 0,
                                  right: 0,
                                  child: Container(
                                    padding: EdgeInsets.all(6),
                                    decoration: BoxDecoration(
                                      color: Colors.white,
                                      shape: BoxShape.circle,
                                    ),
                                    child: Icon(
                                      Icons.edit,
                                      color: Colors.black,
                                      size: 20,
                                    ),
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                        const SizedBox(height: 20),

                        // Name Field
                        _buildTextField('Name', _nameController),
                        const SizedBox(height: 15),

                        // Email Field
                        _buildTextField('Email', _emailController),
                        const SizedBox(height: 15),

                        // Phone Field
                        _buildTextField('Phone Number', _phoneController),
                        const SizedBox(height: 15),

                        // Location Field
                        _buildTextField('Location', _locationController),
                      ],
                    ),
                  ),
                  const SizedBox(height: 20),

                  // Save Button
                  ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Color(0xFF65A3B8),
                      foregroundColor: Colors.white,
                      padding: const EdgeInsets.symmetric(
                          vertical: 16, horizontal: 16),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(8),
                      ),
                      side: const BorderSide(color: Colors.white, width: 2),
                      shadowColor: Colors.black,
                      elevation: 10,
                      minimumSize: const Size(double.infinity, 60),
                    ),
                    onPressed: _updateProfile,
                    child: Text(
                      'Save Changes',
                      style: TextStyle(
                        fontFamily: 'Kanit',
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                        letterSpacing: 1,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildTextField(String label, TextEditingController controller) {
    return TextFormField(
      controller: controller,
      style: TextStyle(color: Colors.white),
      decoration: InputDecoration(
        labelText: label,
        labelStyle: TextStyle(color: Colors.white70),
        enabledBorder: OutlineInputBorder(
          borderSide: BorderSide(color: Colors.white70),
          borderRadius: BorderRadius.circular(8),
        ),
        focusedBorder: OutlineInputBorder(
          borderSide: BorderSide(color: Colors.white),
          borderRadius: BorderRadius.circular(8),
        ),
      ),
      validator: (value) => value!.isEmpty ? 'Please enter $label' : null,
    );
  }
}
