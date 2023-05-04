import 'package:flutter/material.dart';
import 'package:tender_app_windy/src/theme_manager/color_manager.dart';
import 'package:tender_app_windy/src/theme_manager/style_manager.dart';

import '../theme_manager/values_manager.dart';

class CustomTextFieldWidget extends StatelessWidget {
  const CustomTextFieldWidget({
    Key? key,
    required this.labelName,
    required this.hintext,
    this.isObsecure = false,
    required this.controller,
  }) : super(key: key);
  final String labelName;
  final String hintext;
  final bool isObsecure;
  final TextEditingController controller;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text(
          labelName,
          style: getWhiteTextStyle(),
        ),
        const SizedBox(
          height: AppSize.s8,
        ),
        TextField(
          controller: controller,
          obscureText: isObsecure,
          style: getWhiteTextStyle(),
          decoration: InputDecoration(
            contentPadding: const EdgeInsets.symmetric(
                vertical: AppPadding.p15, horizontal: AppPadding.p30),
            filled: true,
            fillColor: ColorManager.secondary,
            hintText: hintext,
            hintStyle: getBlack30TextStyle(),
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(AppSize.s50),
            ),
          ),
        ),
        const SizedBox(
          height: AppSize.s14,
        ),
      ],
    );
  }
}
