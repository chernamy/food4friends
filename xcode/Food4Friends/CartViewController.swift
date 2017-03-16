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
    
    override func viewDidLoad() {
        super.viewDidLoad()
        if (true) {
            sellSubview.isHidden = true
            buySubview.isHidden = false
        }
        else {
            sellSubview.isHidden = false
            buySubview.isHidden = true
        }
        
        
        cartTitle.text = "ITEMS SOLD: "

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
