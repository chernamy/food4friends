//
//  ProfileViewController.swift
//  Food4Friends
//
//  Created by Vaish Raman on 3/19/17.
//  Copyright © 2017 Paramount. All rights reserved.
//

import UIKit
import FBSDKCoreKit
import FBSDKLoginKit
import Foundation

class ProfileViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()
        
//        func getFBUserInfo() {
//            let request = FBSDKGraphRequest(graphPath: "me", parameters: ["fields":"email,name, picture.type(large)"], tokenString: LoginSession.sharedInstance.FBToken?.appID, version: "2.8" , httpMethod: "GET");
//            
//            request?.start { (response, result) in
//                switch result {
//                case .success(let value):
//                    print(value.dictionaryValue)
//                case .failed(let error):
//                    print(error)
//                }
//            }
//        }
        

    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
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
