//
//  BuyConfirmationViewController.swift
//  Food4Friends
//
//  Created by Amy Chern on 4/3/17.
//  Copyright © 2017 Paramount. All rights reserved.
//

import UIKit

class BuyConfirmationViewController: UIViewController {
    @IBOutlet weak var FoodItem: UILabel!
    
    @IBOutlet weak var FoodImage: UIImageView!
    @IBOutlet weak var Address: UILabel!
    @IBOutlet weak var ServingsAvail: UILabel!
    @IBOutlet weak var TimeRemaining: UILabel!
    @IBOutlet weak var Price: UILabel!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        FoodItem.text = globalItemBought
        Address.text = globalAddress
        ServingsAvail.text = globalAvailServings
        TimeRemaining.text = globalTimeLeft
        Price.text = globalPrice
        FoodImage.image = UIImage(data: globalImageData!)
        
        //Looks for single or multiple taps.
        let tap: UITapGestureRecognizer = UITapGestureRecognizer(target: self, action: "dismissKeyboard")
        tap.cancelsTouchesInView = false
        view.addGestureRecognizer(tap)
        
        
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
