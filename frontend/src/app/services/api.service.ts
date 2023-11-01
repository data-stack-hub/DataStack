import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { catchError, tap } from 'rxjs/operators';


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
    // options.params['session_id'] = this.get_session_id()
    return this.http.get(url, options).pipe(tap((data:any)=>{
      // localStorage.setItem('session_id',(data?.appstate?.session_id || 'default'))
    }))
  }

  post(url:any, data:any={}){
    console.log(url, data)
    data['session_id']= this.get_session_id()
    return this.http.post(url, data).pipe(tap((data:any)=>{
      localStorage.setItem('session_id',data.appstate?.session_id)
    }, catchError(this.eh)))
  }
  eh(error){
    console.log(error)
    return 'a'
}
  get_session_id(){
    let id = localStorage.getItem('session_id')
    console.log(id)
    if (id == null || id == undefined || id == 'undefined'){
      console.log('id is null')
      return ''
    }
    else {
      return id
    }
  }
}
