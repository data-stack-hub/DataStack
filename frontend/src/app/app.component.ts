import { Component } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { Subject } from 'rxjs';
import { Observable } from 'rxjs/internal/Observable';
import { map } from 'rxjs/operators';
import { ApiService } from './services/api.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'frontend';
  container:any
  sidebar:any

  constructor(private api:ApiService, public sanitizer: DomSanitizer){
    this.api.get('http://localhost:5000/')
    .subscribe((res:any)=>{
      this.container = JSON.parse(JSON.stringify(res.filter((element:any)=>element.location != 'sidebar')))
      this.sidebar = res.filter((element:any)=>element.location == 'sidebar')
      console.log(this.container, this.sidebar)
    })
  }

  click(e:any){
    console.log(this.container.value)
    this.req(e, '')
  }

  input_change(e:any, event:any){
    console.log(event.target.value)
    // this.container = this.api.post('http://localhost:5000/run_fn',{...e, ...{"payload":event.target.value}})
    this.req(e,event.target.value)
  }

  onSelected(e:any, value:any){
    console.log(value, e)
    this.req(e, value)
  }

  list_click(e:any,value:any){
    this.req(e, value)
  }

  req(e:any, payload:any){
    
    this.api.post('http://localhost:5000/run_fn',{...e, ...{"payload":payload}})
    .subscribe((res:any)=>{
      console.log('resp')
      this.container = JSON.parse(JSON.stringify(res.filter((element:any)=>element.location != 'sidebar')))
      this.sidebar = res.filter((element:any)=>element.location == 'sidebar')

    })
  }

  trackElement(i:any, d:any){
    return i
  }
  public counter = 21;

  public handleOnClick(stateCounter: number) {
    this.counter++;
  }

}
