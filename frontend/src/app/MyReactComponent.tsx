// import * as React from 'react';
// import { FunctionComponent, useEffect, useRef, useState } from 'react';


// // import ReactMarkdown from 'react-markdown'
// export interface IMyComponentProps {
//   counter: number;
//   onClick?: () => void;
// }

// export const MyReactComponent: FunctionComponent<IMyComponentProps> = (props: IMyComponentProps) => {

//   const timerHandle = useRef<number | null>(null);
//   const [stateCounter, setStateCounter] = useState(42);

//   useEffect(() => {
//     timerHandle.current = +setInterval(() => {
//       setStateCounter(stateCounter + 1);
//     }, 2500);

//     return () => {
//       if (timerHandle.current) {
//         clearInterval(timerHandle.current);
//         timerHandle.current = null;
//       }
//     };
//   });

//   const {counter: propsCounter, onClick} = props;

//   const my_json_object = {
//     "a":"a",
//     b:{c:"d"}
//   }
//   const handleClick = () => {
//     console.log('click')
//     setStateCounter(stateCounter + 10)
//     if (onClick) {
        
//       onClick();
//     }
//   };

//   return <div className={`my-graph-component`}>
//     <div className={'comp-props'}>Props counter: {propsCounter}
//       <span onClick={handleClick}
//             className={'increase-button'}>click to increase</span>
//     </div>
  
//     <div className={'comp-state'}>State counter: {stateCounter}</div>

//     {/* <ReactMarkdown># Hello, *world*!</ReactMarkdown> */}
//   </div>;
// };
