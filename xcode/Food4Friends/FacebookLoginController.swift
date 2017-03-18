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

class FacebookLoginController: UIViewController {
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        
        if (FBSDKAccessToken.current() != nil ) {
            // User is logged in, do work such as go to next view controller.
            let viewController = self.storyboard!.instantiateViewController(withIdentifier: "homePage") as UIViewController
            self.present(viewController, animated: true, completion: nil)
        }
        else {
            let loginButton = FBSDKLoginButton()
            loginButton.readPermissions = ["public_profile", "email", "user_friends"]
            // Optional: Place the button in the center of your view.
            loginButton.center = self.view.center
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
            let viewController = self.storyboard!.instantiateViewController(withIdentifier: "tabView") as UIViewController
            self.present(viewController, animated: true, completion: nil)
        }
    }
    
//    override func viewDidAppear(_ animated: Bool) {
//        sleep(2)
//        print("view appears")
//        if (FBSDKAccessToken.current() != nil ) {
//            // User is logged in, do work such as go to next view controller.
//            let viewController = self.storyboard!.instantiateViewController(withIdentifier: "homePage") as UIViewController
//            self.present(viewController, animated: true, completion: nil)
//        }
//        else {
//            print("not logged in")
//        }
//    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
}

