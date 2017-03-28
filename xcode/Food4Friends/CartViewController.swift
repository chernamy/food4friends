//
//  CartViewController.swift
//  Food4Friends
//
//  Created by Vaish Raman on 3/15/17.
//  Copyright © 2017 Paramount. All rights reserved.
//

import UIKit
import Alamofire

class CartViewController: UIViewController {
    @IBOutlet weak var buySubview: UIView!
    @IBOutlet weak var sellSubview: UIView!
    @IBOutlet weak var label: UILabel!

    override func viewDidLoad() {
        
        super.viewDidLoad()

        buySubview.isHidden = true
        sellSubview.isHidden = true
        label.isHidden = true
        
        Alamofire.request(server + "/api/v1/user/", parameters: ["userid": userid], encoding: URLEncoding.default).responseJSON { (response) in
            
            self.buySubview.isHidden = false
            self.sellSubview.isHidden = false
            self.label.isHidden = false
            
            // TODO: Somehow get role
            let role = "seller"
            
            if (role == "none") {
                self.buySubview.removeFromSuperview()
                self.sellSubview.removeFromSuperview()
                self.label.text = "No Transaction In Progress"
            }
            
            else if (role == "buyer") {
                self.sellSubview.removeFromSuperview()
            }
                
            else if (role == "seller") {
                self.buySubview.removeFromSuperview()
            }
            else {
                print("ERROR role not real")
                print(response)
            }
        }
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
}
