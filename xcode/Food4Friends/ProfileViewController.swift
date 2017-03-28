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
import Alamofire

class ProfileViewController: UIViewController {
    @IBAction func logout(_ sender: Any) {
//        FBSDKLoginManager.logOut()
        userid = ""
        userToken = ""
        let loginManager = FBSDKLoginManager()
        loginManager.logOut()
        self.dismiss(animated: false, completion: nil)
    }
    
    func getDataFromUrl(url: URL, completion: @escaping (_ data: Data?, _  response: URLResponse?, _ error: Error?) -> Void) {
        URLSession.shared.dataTask(with: url) {
            (data, response, error) in
            completion(data, response, error)
            }.resume()
    }

    @IBOutlet weak var name: UILabel!
    @IBOutlet weak var propic: UIImageView!
    @IBOutlet weak var email: UILabel!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        let request = FBSDKGraphRequest(graphPath: "me", parameters: ["fields":"email,name, picture.type(large)"], tokenString: userToken, version: nil , httpMethod: "GET");
    
        request?.start(completionHandler: { [weak self] connection, result, error in
            if error != nil {
                print(error?.localizedDescription)
                return
            }
            else{
                let fbResult = result as! Dictionary<String, AnyObject>
                print(fbResult)
                
                self?.name.text = fbResult["name"] as! String?
                self?.email.text = "Email: " + (fbResult["email"] as! String?)!
                
                let pic = fbResult["picture"]
                let data = pic?["data"] as! Dictionary<String, AnyObject>
                let url = URL(string: data["url"] as! String)
                
                self?.getDataFromUrl(url: url!) { (data, response, error)  in
                    guard let data = data, error == nil else { return }
                    print(response?.suggestedFilename ?? url?.lastPathComponent ?? "no response")
                    self?.propic.image = UIImage(data: data)
                }
            }
            
        })
        
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
