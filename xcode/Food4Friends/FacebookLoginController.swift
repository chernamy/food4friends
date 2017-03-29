//
//  FacebookLoginController.swift
//  Food4Friends
//
//  Created by Vaish Raman on 2/1/17.
//  Copyright © 2017 Paramount. All rights reserved.
//


import UIKit
import FBSDKCoreKit
import FBSDKLoginKit
import Foundation

var userToken = ""
var userid = ""
var server = "http://7b713d3f.ngrok.io"

class FacebookLoginController: UIViewController {
    var ConfirmClickResponse = ""
    func makePOSTCall(jsonDict: Dictionary<String, Any>, api_route: String, login: Bool) {
        let loginurl = URL(string: server + api_route)!
        
        let request = NSMutableURLRequest(url: loginurl)
        request.httpMethod = "POST"
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")
        
        if let jsonData = try? JSONSerialization.data(withJSONObject: jsonDict, options: .prettyPrinted) {
            request.httpBody = jsonData
        }
        
        let task = URLSession.shared.dataTask(with: request as URLRequest){ data,response,error in
            if error != nil{
                print("buypageviewcontroller POST session creation error: ")
                print(error?.localizedDescription)
                self.ConfirmClickResponse = "error"
                return
            }
            
            do {
                if let json = try JSONSerialization.jsonObject(with: data!, options: .mutableContainers) as? NSDictionary {
                    if (json["error"] != nil) {
                        print("jsonseriaization error: ")
                        print(json["error"])
                        self.ConfirmClickResponse = "error"
                        
                    } else {
                        let resultValue:String = json["info"] as! String;
                        print("result: \(resultValue)")
                        if (self.ConfirmClickResponse == "") {
                            let viewController = self.storyboard!.instantiateViewController(withIdentifier: "tabView") as UIViewController
                            self.present(viewController, animated: true, completion: nil)
                        }
                    }
                }
            } catch let error as NSError {
                print("buypageviewcontroller POST catch error: ")
                print(error)
                self.ConfirmClickResponse = "error"
            }
        }
        task.resume()
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        
        if (FBSDKAccessToken.current() != nil ) {
            // User is logged in, do work such as go to next view controller.
            let viewController = self.storyboard!.instantiateViewController(withIdentifier: "tabView") as UIViewController
            self.present(viewController, animated: true, completion: nil)
        }
        else {
            let loginButton = FBSDKLoginButton()
            loginButton.readPermissions = ["public_profile", "email", "user_friends"]
            // Optional: Place the button in the center of your view.
            loginButton.center = CGPoint(x: 187.5, y: 500);
            self.view.addSubview(loginButton)
            FBSDKProfile.enableUpdates(onAccessTokenChange: true)
            NotificationCenter.default.addObserver(self, selector: #selector(onTokenUpdated), name: NSNotification.Name.FBSDKAccessTokenDidChange, object: nil)
        }
    }
    
    func onTokenUpdated(notification: NotificationCenter) {
        if (FBSDKAccessToken.current() != nil ) {
            // User is logged in, do work such as go to next view controller.
            // Store user id and token
            userToken = FBSDKAccessToken.current().tokenString
            userid = FBSDKAccessToken.current().userID
            print(userid)
            let jsonDict = ["userid": userid, "token": userToken] as [String : Any]
            makePOSTCall(jsonDict: jsonDict, api_route: "/api/v1/login/", login: true)
        }
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
}
