import 'package:dio/dio.dart';
import 'dart:convert';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

getAuthToken(String username, String password) async {
  final storage = new FlutterSecureStorage();
  var dio = Dio();
  try {
    var res = await dio.post("http://192.168.0.107:8000/api-token-auth/",
        data: {"username": username, "password": password});
    print(res.data);
    print(res.data['token']);
    await storage.write(
      key: "token",
      value:res.data['token']
    );
    return 1;
  } on DioError catch (e) {
    print("Something Went Wrong");
    // print(e.message);
    return 0;
  }
}
