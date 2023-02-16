import { Component, ElementRef, ViewChild } from '@angular/core';
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
  page = '/page1'
  @ViewChild('editableDiv') editableDiv: any;
  @ViewChild('ul_list') ul_list: any;
  innerHTML:any
  url = 'http://localhost:5000/'
  code_output =''
  query_output: any;
  constructor(private api:ApiService, public sanitizer: DomSanitizer){
    this.api.get('http://localhost:5000/')
    .subscribe((res:any)=>{
      this.update_app(res)
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
      this.update_app(res)
      // console.log('resp')
      // this.container = JSON.parse(JSON.stringify(res[this.page].filter((element:any)=>element.location != 'sidebar')))
      // this.sidebar = res[this.page].filter((element:any)=>element.location == 'sidebar')

    })
  }

  update_app(res:any){
    console.log(res)
    this.page = res['current_page']
    this.container = JSON.parse(JSON.stringify(res[this.page].filter((element:any)=>element.location != 'sidebar')))
    this.sidebar = res[this.page].filter((element:any)=>element.location == 'sidebar')
    this.sidebar = [...this.sidebar, ...res['sidebar']]
    console.log(this.container, this.sidebar)
  }

  trackElement(i:any, d:any){
    return i
  }
  public counter = 21;

  public handleOnClick(stateCounter: number) {
    this.counter++;
  }

  change_editable(e:any, ev:any){
    console.log(ev.target.innerHTML)
    this.innerHTML = this.editableDiv.nativeElement.innerHTML
    this.api.post('http://localhost:5000/editable',{...e,...{'payload':this.innerHTML}}).subscribe(res=>{
      console.log(res)
    })
  }

  add_new_editable_filed(){
    console.log(this.ul_list.nativeElement.innerHTML)
    this.ul_list.nativeElement.innerHTML = this.ul_list.nativeElement.innerHTML + "<li contenteditable></li>"
  }

  run_block(e:any){
    console.log(e)
    this.api.post(this.url + '/run_block', {...e}).subscribe(res=>{
      console.log(res)
      this.code_output = res['res']
    })
  }

  run_query(e:any){
    console.log(e)
    this.api.post(this.url + '/run_query_block', {...e}).subscribe(res=>{
      console.log(res)
      this.query_output = res['res']
    })
  }
}
