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
    override func viewDidLoad() {
        super.viewDidLoad()
        buyertest.text = "buyer"
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
