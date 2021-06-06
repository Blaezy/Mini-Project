import 'dart:convert';
import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:image_picker/image_picker.dart';

class FotoUI extends StatefulWidget {
  @override
  _FotoUIState createState() => _FotoUIState();
}

class _FotoUIState extends State<FotoUI> {
  Image? _imageFile;
  File? image;
  final ImagePicker _picker = ImagePicker();
  String animal = "Here will be json Response";
  String url = "http://10.0.2.2:5000/";

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Flask Test"),
        foregroundColor: Colors.black,
      ),
      body: Center(
        child: Column(
          children: [
            Expanded(
              flex: 1,
              child: Padding(
                padding: EdgeInsets.only(top: 10),
                child: Container(
                  width: MediaQuery.of(context).size.width * 0.8,
                  decoration: BoxDecoration(
                    border: Border.all(color: Colors.blue),
                    borderRadius: BorderRadius.circular(2.0),
                  ),
                  child: Center(
                      child: kIsWeb
                          ? (_imageFile == null
                              ? Text('Here Will be our Image')
                              : _imageFile)
                          : image == null
                              ? Text('Here Will be our Image')
                              : (Image.file(File(image!.path)))),
                ),
              ),
            ),
            SizedBox(
              height: 20,
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                ElevatedButton(
                    onPressed: () async {
                      final response = await http.get(Uri.parse(url), headers: {
                        "Accept": "application/json",
                        "Access-Control-Allow-Origin": "*",
                      });
                      if (response.statusCode == 200) {
                        final decode =
                            jsonDecode(response.body) as Map<String, dynamic>;
                        setState(() {
                          animal = decode['message'];
                        });
                      } else {
                        print('Error Occurred');
                      }
                    },
                    child: Text('Json response ')),
                ElevatedButton(
                    onPressed: () async {
                      final pickedFile =
                          await _picker.getImage(source: ImageSource.gallery);
                      if (!kIsWeb) {
                        setState(() {
                          image = File(pickedFile!.path);
                        });
                      } else {
                        setState(() {
                          _imageFile = Image.network(pickedFile!.path);
                        });
                      }
                    },
                    child: Text('Upload Foto ')),
              ],
            ),
            Expanded(
              flex: 1,
              child: Padding(
                padding: EdgeInsets.only(top: 10, bottom: 10),
                child: Container(
                    width: MediaQuery.of(context).size.width * 0.8,
                    decoration: BoxDecoration(
                      border: Border.all(color: Colors.black),
                      borderRadius: BorderRadius.circular(2.0),
                    ),
                    child: Center(
                      child: Text(
                        animal,
                      ),
                    )),
              ),
            )
          ],
        ),
      ),
    );
  }
}
