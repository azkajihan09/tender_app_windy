import 'package:flutter/material.dart';
import 'package:tender_app_windy/src/features/authentication/presentation/sign_up_age_job_screen.dart';
import 'package:tender_app_windy/src/features/authentication/presentation/sign_up_screen.dart';
import 'package:tender_app_windy/src/features/authentication/presentation/sign_up_upload_photo_screen.dart';
import 'package:tender_app_windy/src/features/likes_you/explore_people_screen.dart';

import 'theme_manager/theme_data_manager.dart';

class AppScreen extends StatefulWidget {
  const AppScreen({
    super.key,
  });

  @override
  State<AppScreen> createState() => _AppScreenState();
}

class _AppScreenState extends State<AppScreen> {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Sarang App',
      theme: getApplicationThemeData(),
      initialRoute: SignUpScreen.routeName,
      routes: {
        SignUpScreen.routeName: (context) => SignUpScreen(),
        SignUpAgeJobScreen.routeName: (context) => SignUpAgeJobScreen(),
        SignUpUploadPhotoScreen.routeName: (context) =>
            const SignUpUploadPhotoScreen(),
        ExplorePeopleScreen.routeName: (context) => ExplorePeopleScreen(),
      },
    );
  }
}
