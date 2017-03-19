    //
//  BuyerCartViewController.swift
//  Food4Friends
//
//  Created by Vaish Raman on 3/15/17.
//  Copyright © 2017 Paramount. All rights reserved.
//

import UIKit

class BuyerCartViewController: UIViewController {
    @IBOutlet weak var buyertest: UILabel!
    var address: Int = 0
    var descrip: String = ""
    var photo: String = ""
    var end: Int = 0
    var userid: String = ""
    var price: Int = 0
    var servings: Int = 0
    
    @IBOutlet weak var ItemName: UILabel!
    @IBOutlet weak var ServingsPurchased: UILabel!
    @IBOutlet weak var TimeRemaining: UILabel!
    
    func populatePage() {
        self.ItemName.text = "Item Purchased: " + self.descrip
        self.ServingsPurchased.text = "Servings Purchaed: " + String(servings)
        self.TimeRemaining.text = "Time Remaining: " + String(end)
    }
    
    func buyerCartGETCall() {
        let todoEndpoint: String = server + "/api/v1/buy/current/"
        guard let url = URL(string: todoEndpoint) else {
            print("Error: cannot create URL")
            return
        }
        let urlRequest = URLRequest(url: url)
        
        let config = URLSessionConfiguration.default
        let session = URLSession(configuration: config)
        
        let task = session.dataTask(with: urlRequest, completionHandler: {
            (data, response, error) in
            // do stuff with response, data & error here
            // check for any errors
            guard error == nil else {
                print("error calling GET on /api/v1/buy/current/")
                print(error)
                return
            }
            // make sure we got data
            guard let responseData = data else {
                print("Error: did not receive data")
                return
            }
            do {
                guard let todo = try JSONSerialization.jsonObject(with: responseData, options: []) as? [String: AnyObject] else {
                    print(responseData.description)
                    print("error trying to convert data to JSON")
                    return
                }
                
                //TODO: add to addresses array
                if let arrJSON = todo["items"] as? NSArray{
                    print(arrJSON.count)
                    if(arrJSON.count != 0) {
                        for item in (arrJSON as? [[String:Any]])!{
                            print(item)
                            //self.address = item["address"]
                            self.descrip = item["description"] as! String
                            self.photo = item["photo"] as! String
                            self.end = item["end"] as! Int 
                            self.userid = item["userid"] as! String
                            self.price = item["price"] as! Int
                            self.servings = item["servings"] as! Int
                        }
                    }
                    DispatchQueue.main.async() {
                        self.populatePage()
                        print("successfully populated labels")
                    }
                }
                
            } catch {
                print("error trying to convert data to JSON")
                return
            }
        })
        
        task.resume()
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        self.buyerCartGETCall()
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
