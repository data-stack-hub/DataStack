import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';


@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient) { }

  get(url:any, params:any={}){
    console.log(url, params)
    let options = {
      params:params
    }
    return this.http.get(url, options)
  }

  post(url:any, data:any={}){
    console.log(url, data)
    return this.http.post(url, data)
  }
}
