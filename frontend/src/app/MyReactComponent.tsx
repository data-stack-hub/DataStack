import * as React from 'react';
import { FunctionComponent, useEffect, useRef, useState } from 'react';
import {Client as Styletron} from 'styletron-engine-monolithic';
import { Provider as StyletronProvider } from 'styletron-react';
import { LightTheme, BaseProvider, styled } from 'baseui';
import { StatefulInput } from 'baseui/input';
// import Button from '@material-ui/core/Button'; 
import { Button } from "baseui/button";

import ReactJson from 'react-json-view'
// import ReactMarkdown from 'react-markdown'
export interface IMyComponentProps {
  counter: number;
  onClick?: () => void;
}

export const MyReactComponent: FunctionComponent<IMyComponentProps> = (props: IMyComponentProps) => {

  const timerHandle = useRef<number | null>(null);
  const [stateCounter, setStateCounter] = useState(42);

  useEffect(() => {
    timerHandle.current = +setInterval(() => {
      setStateCounter(stateCounter + 1);
    }, 2500);

    return () => {
      if (timerHandle.current) {
        clearInterval(timerHandle.current);
        timerHandle.current = null;
      }
    };
  });

  const {counter: propsCounter, onClick} = props;
  const engine = new Styletron();
  const my_json_object = {
    "a":"a",
    b:{c:"d"}
  }
  const handleClick = () => {
    console.log('click')
    setStateCounter(stateCounter + 10)
    if (onClick) {
        
      onClick();
    }
  };

  return <div className={`my-graph-component`}>
    <div className={'comp-props'}>Props counter: {propsCounter}
      <span onClick={handleClick}
            className={'increase-button'}>click to increase</span>
    </div>
    <StyletronProvider value={engine}>
      <BaseProvider theme={LightTheme}>
        {/* <Centered> */}
          <StatefulInput />
        {/* </Centered> */}
      </BaseProvider>
    </StyletronProvider>
    <Button  onClick={handleClick}>Click</Button>
    <div className={'comp-state'}>State counter: {stateCounter}</div>
    <ReactJson 
    src={my_json_object} 
    displayDataTypes={false}
    displayObjectSize={false}
    />
    {/* <ReactMarkdown># Hello, *world*!</ReactMarkdown> */}
  </div>;
};
