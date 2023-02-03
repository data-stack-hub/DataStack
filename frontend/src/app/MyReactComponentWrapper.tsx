import {
    AfterViewInit,
    Component,
    ElementRef,
    EventEmitter,
    Input,
    OnChanges,
    OnDestroy,
    Output,
    SimpleChanges,
    ViewChild,
    ViewEncapsulation
  } from '@angular/core';
  import { MyReactComponent } from './MyReactComponent';
  import * as React from 'react';
  
  import * as ReactDOM from 'react-dom';
  
  const containerElementName = 'myReactComponentContainer';
  
  @Component({
    selector: 'app-my-component',
    template: `<span #${containerElementName}></span>`,
    encapsulation: ViewEncapsulation.None,
  })
  export class MyComponentWrapperComponent implements OnChanges, OnDestroy, AfterViewInit {
    @ViewChild(containerElementName, {static: false}) containerRef: ElementRef | any;
  
    @Input() public counter = 10;
    @Output() public componentClick = new EventEmitter<void>();
  
    constructor() {
      this.handleDivClicked = this.handleDivClicked.bind(this);
    }
  
    public handleDivClicked() {
      if (this.componentClick) {
        this.componentClick.emit();
        this.render();
      }
    }
  
    ngOnChanges(changes: SimpleChanges): void {
      this.render();
    }
  
    ngAfterViewInit() {
      this.render();
    }
  
    ngOnDestroy() {
      ReactDOM.unmountComponentAtNode(this.containerRef.nativeElement);
    }
  
    private render() {
      const {counter} = this;
  
    //   ReactDOM.render(<div className={'i-am-classy'}>
    //     <MyReactComponent counter={counter} onClick={this.handleDivClicked}/>
    //   </div>, this.containerRef.nativeElement);

    ReactDOM.render(React.createElement(MyReactComponent), this.containerRef.nativeElement)
    
    }
  }