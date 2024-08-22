function InputBox(placeholder, className ,respectiveEvent ,inputType , stateVariableToUpdate )
{
    const eventHandler = {
        [respectiveEvent]: (e) => { stateVariableToUpdate(e.target.value) }
    };

   return ( <input type ={inputType} placeholder={placeholder} className={className} {...eventHandler} />  )
}


export default InputBox