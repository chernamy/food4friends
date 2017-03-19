//
//  SellnfoViewController.swift
//  Food4Friends
//
//  Created by Vaish Raman on 3/13/17.
//  Copyright © 2017 Paramount. All rights reserved.
//

import UIKit

class SellnfoViewController: UIViewController {
    
    @IBOutlet weak var foodPic: UIImageView!
    @IBOutlet weak var itemDescription: UITextField!
    @IBOutlet weak var servings: UITextField!
    @IBOutlet weak var price: UITextField!
    @IBOutlet weak var address: UITextField!
    @IBOutlet weak var durationMin: UITextField!
    
    @IBAction func sellFood(_ sender: Any) {
        var request = URLRequest(url: URL(string: server + "/api/v1/sell/")!)
        request.httpMethod = "POST"
        let postString = "userid=" + LoginSession.sharedInstance.userId! + "&servings=" + servings.text! + "&duration=" + durationMin.text! + "&price=" + price.text! + "&address=" + address.text! + "&description" + itemDescription.text!
        request.httpBody = postString.data(using: .utf8)
        request.setValue("multipart/form-data", forHTTPHeaderField: "Content-Type")
        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            guard let data = data else {
                print("error getting data")
                return
            }
            
            if let httpStatus = response as? HTTPURLResponse,
                httpStatus.statusCode != 200 {
                print("statusCode should be 200, but is \(httpStatus.statusCode)")
                print("response = \(response)")
                self.tabBarController?.selectedIndex = 3;
            }
            let responseString = String(data: data, encoding: .utf8)
            print ("response String")
            print (responseString ?? "No string")
        }
        task.resume()
        
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
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}






