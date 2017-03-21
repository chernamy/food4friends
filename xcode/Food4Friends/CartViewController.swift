//
//  CartViewController.swift
//  Food4Friends
//
//  Created by Vaish Raman on 3/15/17.
//  Copyright © 2017 Paramount. All rights reserved.
//

import UIKit

class CartViewController: UIViewController {
    @IBOutlet weak var buySubview: UIView!
    @IBOutlet weak var sellSubview: UIView!
    @IBOutlet weak var cartTitle: UILabel!
    @IBOutlet weak var servingsInfo: UILabel!
    @IBOutlet weak var timeLeft: UILabel!
    
    func GETCall(params: [String:String]) {
        let userurl = URL(string: server + "/api/v1/user/")!
        
        let request = NSMutableURLRequest(url: userurl)
        request.httpMethod = "GET"
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let jsonDict = ["userid":userid] as [String : Any]
        
        if let jsonData = try? JSONSerialization.data(withJSONObject: jsonDict, options: .prettyPrinted) {
            request.httpBody = jsonData
        }
        
        let task = URLSession.shared.dataTask(with: request as URLRequest){ data,response,error in            // do stuff with response, data & error here
            if error != nil{
                print(error?.localizedDescription)
                return
            }
            
            do {
                if let json = try JSONSerialization.jsonObject(with: data!, options: .mutableContainers) as? NSDictionary {
                    if (json["error"] != nil) {
                        print(json["error"])
                    } else {
                        let resultValue:String = json["info"] as! String;
                        print("result: \(resultValue)")
                    }
                }
            } catch let error as NSError {
                print(error)
            }
            
        }
        task.resume()
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        if (false) {
            sellSubview.isHidden = true
            buySubview.isHidden = false
        }
        else {
            // Sell Cart Page
            sellSubview.isHidden = false
            buySubview.isHidden = true
            
            
            cartTitle.text = "ITEMS SOLD: "
            servingsInfo.text = "Servings Left: "
            timeLeft.text = "Time Remaining: "
        }
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
