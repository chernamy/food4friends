//
//  SellController.swift
//  Food4Friends
//
//  Created by Vaish Raman on 2/7/17.
//  Copyright © 2017 Paramount. All rights reserved.
//

//
//  SellViewController.swift
//  Food4Friends
//
//  Created by Vaish Raman on 2/12/17.
//  Copyright © 2017 Paramount. All rights reserved.
//

import UIKit

class SellViewController: UIViewController, UIImagePickerControllerDelegate, UINavigationControllerDelegate {
    
    var imageTaken = false
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Do any additional setup after loading the view.
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    override func viewDidAppear(_ animated: Bool) {
        
        if (!imageTaken) {
            
            let imagePicker = UIImagePickerController()
            
            imagePicker.delegate = self
            imagePicker.sourceType = UIImagePickerControllerSourceType.camera
            imagePicker.allowsEditing = false
            
            
            self.present(imagePicker, animated: true,
                         completion: nil)
            
        }
    }
    
//    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [String : Any]) {
//        let image = info[UIImagePickerControllerOriginalImage] as! UIImage
//        imageTaken = true
//        print(image)
//        
//        self.dismiss(animated: true, completion: nil)
//        
//        let sellDescriptionViewController : SellDescriptionViewController = self.storyboard?.instantiateViewController(withIdentifier: "SellDescription") as! SellDescriptionViewController
//        self.present(sellDescriptionViewController, animated: true, completion: nil)
//    }
//    
//    func imagePickerControllerDidCancel(_ picker: UIImagePickerController) {
//        self.dismiss(animated: true, completion: nil)
//    }
    
    
}




