import 'package:flutter/material.dart';
import 'package:tender_app_windy/src/common_widgets/custom_button_widget.dart';
import 'package:tender_app_windy/src/common_widgets/custom_text_button_widget.dart';
import 'package:tender_app_windy/src/common_widgets/logo_and_tagline_widget.dart';
import 'package:tender_app_windy/src/common_widgets/upload_photo_widgte.dart';
import 'package:tender_app_windy/src/features/likes_you/explore_people_screen.dart';
import 'package:tender_app_windy/src/theme_manager/font_manager.dart';
import 'package:tender_app_windy/src/theme_manager/style_manager.dart';
import 'package:tender_app_windy/src/theme_manager/values_manager.dart';

class SignUpUploadPhotoScreen extends StatefulWidget {
  static const String routeName = '/sign-up-upload-photo';
  const SignUpUploadPhotoScreen({super.key});

  @override
  State<SignUpUploadPhotoScreen> createState() =>
      _SignUpUploadPhotoScreenState();
}

class _SignUpUploadPhotoScreenState extends State<SignUpUploadPhotoScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.symmetric(
          vertical: AppPadding.p50,
          horizontal: AppPadding.p24,
        ),
        child: SingleChildScrollView(
          child: Column(
            children: [
              const LogoAndTaglineWidget(),
              const SizedBox(
                height: AppSize.s50,
              ),
              const UploadPhotoWidget(),
              const SizedBox(
                height: AppSize.s28,
              ),
              Text(
                'Andi Mania',
                style: getWhiteTextStyle(
                  fontSize: FontSizeManager.f22,
                  fontWeight: FontWeightManager.semiBold,
                ),
              ),
              const SizedBox(
                height: AppSize.s4,
              ),
              Text(
                '22, Leayer',
                style: getBlack60TextStyle(),
              ),
              const SizedBox(
                height: 240.0,
              ),
              CustomButtonWidget(
                title: 'Update My Profile',
                onTap: () {},
              ),
              const SizedBox(
                height: AppSize.s28,
              ),
              CustomTextButtonWidget(
                title: 'Skip for Now',
                onPressed: () {
                  Navigator.pushNamed(context, ExplorePeopleScreen.routeName);
                },
              )
            ],
          ),
        ),
      ),
    );
  }
}
