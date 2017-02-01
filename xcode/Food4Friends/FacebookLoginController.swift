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

class FacebookLoginController: UIViewController {

    @IBOutlet weak var loginButton: FBSDKLoginButton!

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        
        if (FBSDKAccessToken.current() != nil ) {
            // User is logged in, do work such as go to next view controller.
            
        }
        else {
            let loginButton = FBSDKLoginButton()
            loginButton.readPermissions = ["public_profile", "email", "user_friends"]
            // Optional: Place the button in the center of your view.
            loginButton.center = self.view.center
            self.view.addSubview(loginButton)
            FBSDKProfile.enableUpdates(onAccessTokenChange: true)
            NotificationCenter.default.addObserver(self, selector: Selector(("onProfileUpdated:")), name:NSNotification.Name.FBSDKProfileDidChange, object: nil)
        }
    }
    
    func onProfileUpdated() {
        print("profile updated called")
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
}

