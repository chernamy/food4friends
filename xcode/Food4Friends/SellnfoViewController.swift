//
//  SellnfoViewController.swift
//  Food4Friends
//
//  Created by Vaish Raman on 3/13/17.
//  Copyright © 2017 Paramount. All rights reserved.
//

import UIKit
import Alamofire

class SellnfoViewController: UIViewController {
    
    @IBOutlet weak var foodPic: UIImageView!
    @IBOutlet weak var itemDescription: UITextField!
    @IBOutlet weak var servings: UITextField!
    @IBOutlet weak var price: UITextField!
    @IBOutlet weak var address: UITextField!
    @IBOutlet weak var durationMin: UITextField!
    
    @IBAction func sellFood(_ sender: Any) {
        
        let multipartformdata = MultipartFormData()
        let postDict = ["userid": userid, "servings": servings.text!, "duration": durationMin.text!, "price": price.text!, "address": address.text!, "description": itemDescription.text!] as [String: String]

        do {
            let sell_url = try URLRequest(url: server + "/api/v1/sell/", method: .post, headers: ["Content-Type" : multipartformdata.contentType])
            
            let imageData = UIImagePNGRepresentation(foodPic.image!)!
            
            Alamofire.upload(multipartFormData: { (multipartFormData) in
                multipartFormData.append(imageData, withName: "photo", fileName: "file.png", mimeType: "image/png")
                
                for (key, value) in postDict {
                    multipartFormData.append(value.data(using: String.Encoding.utf8)!, withName: key)
                }
        
            }, with: sell_url) { (result) in
                switch result {
                case .success(let upload, _, _):
                    self.tabBarController?.selectedIndex = 4
                    print(upload)
                case .failure( _):
                    print("no")
                }
            }

        }
        catch {
           print("error occured")
        }
        
        
//        var request = NSMutableURLRequest(url: URL(string: server + "/api/v1/sell/")!)
//        request.httpMethod = "POST"
////        let postDict = ["userid": userid, "servings": servings.text!, "duration": durationMin.text!, "price": price.text!, "address": address.text!, "description": itemDescription.text!] as [String: Any]
//        let boundary = generateBoundaryString()
//
//        request.addValue("application/json", forHTTPHeaderField: "Content-Type")
//
////        request.setValue("multipart/form-data; boundary=\(boundary)",
////            forHTTPHeaderField: "Content-Type")
//        
//        let bodyData = "userid=id&key2=value&key3=value"
//        request.httpBody = bodyData.data(using: String.Encoding.utf8);
//        
//        let task = URLSession.shared.dataTask(with: request as URLRequest) { data, response, error in
//            guard let data = data else {
//                print("error getting data")
//                return
//            }
//            
//            
//            if let httpStatus = response as? HTTPURLResponse,
//                httpStatus.statusCode != 200 {
//                print("statusCode should be 200, but is \(httpStatus.statusCode)")
//                print("response = \(response)")
//            }
//            
//            let responseString = String(data: data, encoding: .utf8)
//            print ("response String")
//            print (responseString ?? "No string")
//            self.tabBarController?.selectedIndex = 3;
//        }
//        
//        task.resume()
//        
        
    }
    


    override func viewDidLoad() {
        super.viewDidLoad()
        foodPic.image = Singleton.sharedInstance.imageValue
        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    func generateBoundaryString() -> String {
        return "Boundary-\(NSUUID().uuidString)"
    }

    func createBodyWithParameters(parameters: [String: Any]?, filePathKey: String?, imageDataKey: Data, boundary: String) -> Data {
        var body = Data();
//        if parameters != nil {
//            for (key, value) in parameters! {
//                var tmp = "--" + boundary + "\r\n"
//                body.append(Data(tmp.utf8))
//                tmp = "Content-Disposition: form-data; name=\"" + key + "\"\r\n\r\n"
//                body.append(Data(tmp.utf8))
//                tmp = String(describing: value) + "\r\n"
//                body.append(Data(tmp.utf8))
//            }
//        }
//        
        
        let filename = "user-profile.png"
        let mimetype = "image/png"
        
        body.append("--\(boundary)\r\n".data(using: String.Encoding.utf8)!)
        body.append("Content-Disposition:form-data;name=\"photo\"\r\n\r\n".data(using: String.Encoding.utf8)!)
        body.append("Incoming\r\n".data(using: String.Encoding.utf8)!)
        body.append("--\(boundary)\r\n".data(using: String.Encoding.utf8)!)
        body.append("Content-Disposition:form-data; name=\"file\";filename=\"\(filename)\"\r\n".data(using: String.Encoding.utf8)!)
        body.append("Content-Type: \(mimetype)\r\n\r\n".data(using:String.Encoding.utf8)!)
        body.append(imageDataKey)
        body.append("\r\n".data(using: String.Encoding.utf8)!)
        body.append("--\(boundary)--\r\n".data(using:
            String.Encoding.utf8)!)
        return body
    }

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}






