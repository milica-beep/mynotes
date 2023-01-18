import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { map } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  serverUrl:string = "http://127.0.0.1:5000/";
  constructor(private http: HttpClient) { }

  public getToken(): any {
    return localStorage.getItem('accessToken');
  }

  login(email:string, password:string) {
    return this.http.post<any>(this.serverUrl+'/auth/login', {email: email, password: password})
    .pipe(map(response => {
      localStorage.setItem('accessToken', response.access_token);
      return response;
    }))
  }
  
  register(name:string, lastname:string, email:string, password:string) {
    let user = {
      name: name,
      lastname: lastname,
      email: email,
      password: password
    }
    return this.http.post(this.serverUrl + 'auth/register', user);
  }

  getCurrentUser() {
    return this.http.get<any>(this.serverUrl + "auth/current-user");
  }
}
