//
//  ContentView.swift
//  Shared
//
//  Created by Ryan Roth on 3/7/24.
//

import SwiftUI

struct ContentView: View {
    @State private var firstName: String = "Phlip"
    @State private var lastName: String = "Norbalnd"
    @State private var username: String = "pnorb"
    @State private var password: String = "test123"
    
    var body: some View {
        VStack {
            Text("Hello!")
                .padding()
            
            TextField("First Name", text: $firstName)
                .padding()
            
            TextField("Last Name", text: $lastName)
                .padding()
            
            TextField("Username", text: $username)
                .padding()
            
            SecureField("Password", text: $password)
                .padding()
            
            Button(action: {
                // Action to perform when the button is tapped
                sendDataToBackend()
            }) {
                Text("Send Data to Backend")
                    .padding()
                    .background(Color.blue)
                    .foregroundColor(Color.white)
                    .cornerRadius(10)
            }
        }
        .padding()
    }
    
    func sendDataToBackend() {
        guard let url = URL(string: "http://localhost:4000/set_user") else {
            print("Invalid URL")
            return
        }
        
        let userData = [
            "name_first": firstName,
            "name_last": lastName,
            "username": username,
            "password": password
        ]
        
    
        
        guard let jsonData = try? JSONSerialization.data(withJSONObject: userData) else {
            print("Error serializing JSON")
            return
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = jsonData
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                print("Error: \(error.localizedDescription)")
                return
            }
            
            if let response = response as? HTTPURLResponse {
                print("Response status code: \(response.statusCode)")
            }
            
            if let data = data {
                if let responseString = String(data: data, encoding: .utf8) {
                    print("Response data: \(responseString)")
                }
            }
        }.resume()
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
