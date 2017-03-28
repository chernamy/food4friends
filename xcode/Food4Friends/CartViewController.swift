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
    @IBOutlet weak var cartTitle: UILabel!
    @IBOutlet weak var servingsInfo: UILabel!
    @IBOutlet weak var timeLeft: UILabel!

    override func viewDidLoad() {
        super.viewDidLoad()
        
        // remove both subviews from superview
        for view in self.view.subviews {
            view.removeFromSuperview()
        }
        
        Alamofire.request(server + "/api/v1/user/", parameters: ["userid": userid], encoding: JSONEncoding.default).responseJSON { (response) in
            print("GOT USER INFO")
            print(response)
        }
        
//        self.view.addSubview(buySubview)
//        self.view.addSubview(sellSubview)
    
        
//        if (false) {
//        }
//        else {
//            // Sell Cart Page
//            sellSubview.isHidden = false
//            buySubview.isHidden = true
//            
////            
////            cartTitle.text = "Sold: Noodles & Broccoli"
////            servingsInfo.text = "Servings Left: 18"
////            timeLeft.text = "Time Remaining: 20 min"
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
