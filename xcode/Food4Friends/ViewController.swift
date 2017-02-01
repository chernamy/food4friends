//
//  ViewController.swift
//  Food4Friends
//
//  Created by Vaish Raman on 1/27/17.
//  Copyright © 2017 Paramount. All rights reserved.
//

import UIKit

import FBSDKCoreKit
import FBSDKLoginKit

class ViewController: UIViewController, UIImagePickerControllerDelegate, UINavigationControllerDelegate {

    @IBOutlet weak var foodImage: UIImageView!
    @IBOutlet weak var sellButton: UIButton!

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    @IBAction func CameraAction(_ sender: UIButton) {
        let imagePicker = UIImagePickerController()
        
        imagePicker.delegate = self
        imagePicker.sourceType = UIImagePickerControllerSourceType.camera
        imagePicker.allowsEditing = false
        
        
        self.present(imagePicker, animated: true,
                     completion: nil)
        
        func imagePickerController(picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [String : Any]) {
            let image = info[UIImagePickerControllerOriginalImage] as! UIImage
            print(image)
            foodImage.image = image
            dismiss(animated: true, completion: nil)
        }
        
        func imagePickerControllerDidCancel(_ picker: UIImagePickerController) {
            self.dismiss(animated: true, completion: nil)
        }
        
    }
}

