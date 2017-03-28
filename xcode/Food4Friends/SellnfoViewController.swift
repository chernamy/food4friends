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
    
}
