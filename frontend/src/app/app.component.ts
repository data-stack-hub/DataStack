import { Component, ElementRef, Renderer2, ViewChild } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { Subject } from 'rxjs';
import { Observable } from 'rxjs/internal/Observable';
import { map } from 'rxjs/operators';
import { formatISO,isAfter,isBefore } from "date-fns";
import { ApiService } from './services/api.service';
declare const monaco: any;
import { marked } from 'marked';
import { NzNotificationService } from 'ng-zorro-antd/notification';
import { AngularGridInstance, Column, GridOption } from 'angular-slickgrid';
import { ExcelExportService } from '@slickgrid-universal/excel-export';

interface trace {
  x:Array<any>,
  y:Array<any>,
  type: string,
  mode:any,
  marker:{size?:any, color:any, line?:{width:any}}

}
interface  g {
  data:Array<trace>,
  layout:any
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})


export class AppComponent {
  date_value: Date;
  title = 'frontend';
  container:any
  sidebar:any
  appstate:any
  page = '/page1'
  @ViewChild('editableDiv') editableDiv: any;
  @ViewChild('ul_list') ul_list: any;
  innerHTML:any
  url = 'https://localhost:5000/'
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
  spinning = false
  app_loading = true
  app_error = false
  columnDefinitions: Column[] = [];
  gridOptions: GridOption = {};
  dataset: any[] = [];

  public graph = {
    data: [
        { x: [1, 2, 3,4,5,6,7,8,9], y: [2, 6, 3,5,4,3,6,8], type: 'scatter', mode: 'lines+markers', marker: {color: 'red'} },
        { x: [6,3,7,3,6], y: [2,5,2,6,3], type: 'scatter' , mode: 'lines+markers', marker: {color: 'blue'} },
    ],
    layout: { title: 'A Fancy Plot', 'xaxis':{'type':'category'}},
    config : {editable:true, responsive: true}
};
  angularGrid: AngularGridInstance;

  constructor(private api:ApiService, public sanitizer: DomSanitizer, public renderer: Renderer2, public notification:NzNotificationService){
    console.log(window.location.protocol)
    let host = window.location.hostname
    let port
    if (Number(window.location.port) == 4200){
      port = 5000
    } else if (window.location.port){
      port = Number(window.location.port)
    } else {
      port = this.isHttps() ? 443 : 80
    }

    let basepath = window.location.pathname.replace("/\/+$/","").replace("/^\/+/","")
    this.url = window.location.protocol + "//" + host +":" + port +"/"
    console.log(window.location.hostname,window.location.port, window.location.pathname )
    this.api.get(this.url +'app')
    .subscribe((res:any)=>{
      this.update_app(res)
      this.app_loading= false
    }, (error)=>{
      console.log('error:', error)
      this.app_loading = false
      this.app_error = true
    })

    this.prepareGrid();
  }


 isHttps(): boolean {
  return window.location.href.startsWith("https://")
}
  click(e:any){
    console.log(this.container.value)
    this.req(e, '')

  }

  input_change(e:any, event:any){
    console.log(event.target.value)
    // this.container = this.api.post('http://localhost:5000/run_fn',{...e, ...{"payload":event.target.value}})
    this.req(e,{value : event.target.value, action:'change'})
  }

  menu_click(e:any, value){
    this.req(e, {value: value, action:'change'})
  }

  onSelected(e:any, value:any){
    console.log(value, e)
    this.req(e, {value: value, action:'change'})
  }

  list_click(e:any,value:any){
    this.req(e, {value:value, action:"click"})
  }

  req(e:any, payload:any){
    this.spinning = true
    console.log(payload)
    this.api.post(this.url + 'run_fn',{...e, ...{"payload":payload}})
    .subscribe((res:any)=>{
      console.log(res)
      this.spinning = false
      this.update_app(res)
      // console.log('resp')
      // this.container = JSON.parse(JSON.stringify(res[this.page].filter((element:any)=>element.location != 'sidebar')))
      // this.sidebar = res[this.page].filter((element:any)=>element.location == 'sidebar')

    })
  }

  update_app(res:any){
    console.log(res)
    let all_elements = []
    let all_pages = ['main_page'].concat(res['pages'])
    console.log(all_pages)
    all_pages.forEach(page=>{
      this.str_to_json_fix(res[page].concat(all_elements))

    })

    this.page = res['current_page']
    this.container = JSON.parse(JSON.stringify(res[this.page].filter((element:any)=>element.location != 'sidebar')))
    this.sidebar = res[this.page].filter((element:any)=>element.location == 'sidebar')
    this.sidebar = [...this.sidebar, ...res['sidebar']]
    this.appstate = res['appstate']
    if(this.appstate.notifications && this.appstate.notifications.length > 0){
      this.appstate.notifications.forEach(element => {
        this.notify(element)
      });
    }

    console.log(res)
  }

  str_to_json_fix(list){
    console.log(list)
    list.forEach(element => {
      if (false){
        element.prop.data = JSON.parse(element.prop.data)
        if (element['type'] == 'chart'){
          // element.prop.data.data[0].marker.size = 12
        }
      }
      // if (element['type']== 'dataframe' ){
      //   console.log(element.prop.columns)
      //   element.prop.columns = JSON.parse(element.prop.columns)

      // }
      if (element['type'] == 'expander'){
        this.str_to_json_fix(element['data'])
      }
      if (element['type'] == 'column'){
        element['data'].forEach(element1 => {
          this.str_to_json_fix(element1)
        });

      }
    });

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
    this.api.post(this.url + 'editable',{...e,...{'payload':this.innerHTML}}).subscribe(res=>{
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


  update_chart(obj ,key, event){
    console.log(obj, event)
    var keys = key.split(".");
    console.log(keys)
    var propertyName = keys.pop();
    var propertyParent = obj;

    while (keys.length > 0) {
      console.log(keys, propertyParent)
      let k = keys.shift()
      let c_propertyParent = propertyParent[k];
      if (c_propertyParent == undefined){
        propertyParent[k] = {}
        propertyParent = propertyParent[k]
      }
      else {
        propertyParent = c_propertyParent
      }

    }
    propertyParent[propertyName] = event;
    console.log(obj)
  }

  get_df_columns(event, trace, axis){
    console.log(event)
    this.api.post(this.url + 'run_block', {prop:{
      // code: "print("+event+".astype(str).values.flatten().tolist())"
      code:"print(" + event +".to_json(orient='split'))"
    } }).subscribe(res=>{
      console.log(JSON.parse(res['res'])['data'])
      this.graph.data[trace][axis] = JSON.parse(res['res'])['data']
      console.log(this.graph.data)
    })
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
    console.log(block, event.target.innerHTML,b, e)
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

    // e.onDidChangeContent((event)=>{
    //   console.log(event)
    // })
    // this.editor.setModel(monaco.editor.createModel("console.log('Hello ng-zorro-antd')", 'typescript'));
    console.log( e.getModel().getLineCount(), e.getContentHeight())
    this.height = e.getContentHeight() +20
    // this.editor.layout()
  }
  rel(e){
    console.log('relouting code editor', e.getContentHeight())
    // this.height = this.editor.getContentHeight()
    // this.editor.layout({height:this.height})

  }

  page_link(element:any){
    this.req(element, '')
  }

  slider_value_changed(element:any, event:any){
    this.req(element,  {value: event, action:'change'})
  }

  date_changed(element:any, event:any){


    this.req(element,{value: formatISO(event, { representation: 'date' }), action:'change'}  )

  }

  date_min_max(min,max){
    if (min && max){
      return (current: Date) => {
        return !current || isAfter(current,new Date(max)) || isBefore(current,new Date(min));
    }
  }else if(min){
    return (current: Date) => {
      return !current || isBefore(current,new Date(min));
  }
  }else if(max){
    return (current: Date) => {
      return !current || isAfter(current,new Date(max));
  }
  }else{
    return (current: Date) => {
      return !current || isAfter(current,new Date('2500-01-01')) || isBefore(current,new Date('1970-01-01'));
  }
  }

}

str_to_json(str){

  if(typeof(str) != 'object'){
  return JSON.parse(str)
  }
  else {
    return str
  }
}

get_marked(data){
  if(typeof(data) =='number'){
    data = String(data)
  }
  return marked(data)
}

notify(data){
  // this.notification
  // .blank(
  //   'Notification' ,
  //   data.data
  // )

}

angularGridReady(angularGrid: AngularGridInstance) {
  console.log(angularGrid)
  this.angularGrid = angularGrid;
  this.angularGrid.resizerService.resizeColumnsByCellContent(true);
}

prepareGrid() {
  this.columnDefinitions = [
    { id: 'title_tkrtkrgmdfmgfdmgkfd', name: 'title_tkrtkrgmdfmgfdmgkfd', field: 'title_tkrtkrgmdfmgfdmgkfd', sortable: true },
    { id: 'duration', name: 'Duration (days)', field: 'duration', sortable: true },
    { id: '%', name: '% Complete', field: 'percentComplete', sortable: true },
    { id: 'start', name: 'Start', field: 'start' },
    { id: 'finish', name: 'Finish', field: 'finish' },
  ];

  this.gridOptions =
  {
    enableAutoResize: true,
    autoResize: {
      container: '#demo-container',
      rightPadding: 50
    },
    enableFiltering: true,
    gridHeight:400,
    enableSorting: true,
    enableExcelExport: true,
    registerExternalResources: [new ExcelExportService()] ,
     // resizing by cell content is opt-in
      // we first need to disable the 2 default flags to autoFit/autosize
      autoFitColumnsOnFirstLoad: false,
      enableAutoSizeColumns: false,
    //   // then enable resize by content with these 2 flags
      autosizeColumnsByCellContentOnFirstLoad: true,

      enableAutoResizeColumnsByCellContent: true,

  };


  // fill the dataset with your data (or read it from the DB)
  this.dataset = [
    { id: 0, title_tkrtkrgmdfmgfdmgkfd: 'E0100CTHQ', duration: 45, percentComplete: 5, start: '2001-01-01', finish: '2001-01-31' },
    { id: 1, title_tkrtkrgmdfmgfdmgkfd: 'E0100CTHQ', duration: 33, percentComplete: 34, start: '2001-01-11', finish: '2001-02-04' },
  ];
}

plotly_click(element, event){
  console.log(event)
  event.points.forEach(element => {
  delete element.xaxis
  delete element.yaxis
  delete element.fullData
  });

  this.req(element,  {value: event.points, action:'chart_click'})
}

}











