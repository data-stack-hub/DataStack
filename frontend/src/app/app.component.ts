import { Component, ElementRef, Renderer2, ViewChild } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { Subject } from 'rxjs';
import { Observable } from 'rxjs/internal/Observable';
import { map } from 'rxjs/operators';
import { ApiService } from './services/api.service';
declare const monaco: any;
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
  a = 'h1'
  show_context = false
  current_index:any  = {}
  current_element:any
  editable_page = [
      {
        _id: "5f54d75b114c6d176d7e9765",
        html: "Heading",
        tag: "h1",
        imageUrl: "",
      },
      {
        _id: "5f54d75b114c6d176d7e9766",
        html: "I am a <strong>paragraph</strong>",
        tag: "p",
        imageUrl: "",
      },
      {
        _id: "5f54d75b114c6d176d7e9767",
        html: "/im",
        tag: "p",
        imageUrl: "images/test.png",
      }
    ]
  current_block: any;
  editor: any;
  height =30;
  constructor(private api:ApiService, public sanitizer: DomSanitizer, public renderer: Renderer2){
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
    res['main_page'].forEach(element => {
      if (element['type']== 'dataframe'){
        element.prop.data = JSON.parse(element.prop.data)
      }
    });
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

  change_cell(e:any){
    console.log(e)
    this.api.post(this.url +'editable', {...e,...{'payload':''}}).subscribe(res=>{console.log(res)})
  }

  enter(e:any, index:any, element:any, block:any){

    console.log(index, element['prop']['html'].length,e)
    if(e.key == "Enter" && block['tag'] != 'list'){
      e.preventDefault();
      e.stopPropagation();
    let n ={
      _id: "5f54d75b114c6d176d7e9766a",
      html: "new",
      tag: "p",
      imageUrl: "",
    }
    if (index +1 == element['prop']['html'].length || true){
      this.add_new_block(element, index+1)  
    }
    else{
    let element = e.target.parentElement.nextElementSibling.firstElementChild;
    console.log(element)
    element.focus()
    }
  }
  if(e.key == '/'){
    this.show_context = true
    this.current_block = block
    this.current_element = element
  }
  console.log(block['html'], block['html'].length)
  if ((e.key == 'Backspace' || e.key == 'Delete') && e.target.innerHTML.length == 0){
    this.current_block = block
    this.current_element = element
    this.delete_block(element,index)
  }
  }

  delete_block(element:any, index:any){
    console.log('delete block', this.current_element)
    element['prop']['html'].splice(index, 1);
  }
  update_block(tag:any){
    this.show_context = false
    this.current_block['tag'] = tag
    if (tag == 'list'){
      this.current_block['html'] ="<li></li>"
    }

    if (tag == 'code'){
      let new_block = {
        "_id":this.current_block['_id'],
        "type":'code',
        "prop":{
          "code":"",
        }
      }
      this.current_block = new_block
    }

    if (tag == 'expander'){
      let new_block = {
        "_id":this.current_block['_id'],
        "type":"expander",
        "title":"expander",
        "wid":'databook',
        "prop":{
          "html":[
            {
              "_id":'new_id' + Math.random(),
              "type":'code',
              "wid":"some_id",
              "prop":{
                "code":"",
              }
            }
          ]
        }
      }
      this.current_block = new_block
    }
 
    console.log(this.current_block)
    this.update_on_server(this.current_element, this.current_block,'')
  }
  // current_element(current_element: any, current_block: any) {
  //   throw new Error('Method not implemented.');
  // }

add_new_block(element:any, index:any=-1){
  let new_block = {
    _id:'new_id' + Math.random(),
    html:"new_block",
    tag:"p"
  }
  if (index = -1){
    index = element['prop']['html'].length
  }
  element['prop']['html'].splice(index , 0, new_block);
  // let new_element = this.renderer.createElement(new_block['tag'])
  // new_element.innerHTML = new_block['html']
  // new_element.id = new_block['_id']
  // new_element.contentEditable = true
  // this.renderer.listen(new_element, 'keydown.enter', (event)=>{this.enter(event, element['prop']['html'].length,element,new_block)})
  // this.renderer.listen(new_element, 'click', (event)=>{console.log(event)})
  // this.renderer.appendChild(this.editableDiv.nativeElement ,new_element)
  setTimeout(() => {
    document.getElementById(new_block['_id'])?.focus()
  });
  
}
  block_change(e:any, block:any, event:any){
    console.log(event.target.innerHTML)
  if(event.target.innerhtml == "/"){
    console.log('show')
    this.show_context = true
  }
    let b = Object.assign({}, block)
    b['html'] = event.target.innerHTML
    console.log(block, event.target.innerHTML, e)
    this.update_on_server(e,b, block)
  }

  update_on_server(e:any, payload:any, parent:any){

    let payload_ = {
      block:payload,
      parent:e
    }
    console.log(e, payload_)
    this.api.post(this.url +'editable', {...e,...{'payload':payload_}}).subscribe(res=>{console.log(res)})
  }

  onEditorInit(e: any): void {
    this.editor = e
    e.onDidContentSizeChange(()=>{
      console.log(e.getContentHeight())
      this.height = e.getContentHeight() +20

    });  

    e.onDidChangeContent((event)=>{
      console.log(event)
    })
    // this.editor.setModel(monaco.editor.createModel("console.log('Hello ng-zorro-antd')", 'typescript'));
    console.log( e.getModel().getLineCount())
  }
  rel(e){
    console.log('relouting code editor', e.getContentHeight())
    // this.height = this.editor.getContentHeight()
    // this.editor.layout({height:this.height})
    
  }

}
