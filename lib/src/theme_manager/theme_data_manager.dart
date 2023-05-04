import 'package:flutter/material.dart';
import 'package:tender_app_windy/src/theme_manager/color_manager.dart';
import 'package:tender_app_windy/src/theme_manager/font_manager.dart';

ThemeData getApplicationThemeData() {
  return ThemeData(
    scaffoldBackgroundColor: ColorManager.primary,
    appBarTheme: AppBarTheme(
      backgroundColor: ColorManager.primary,
      elevation: 0,
    ),

    fontFamily: FontFamilyConstant.fontFamily,
  );
}
