// @flow
import * as React from 'react'
import componentStyle from './component.css'

type Props = {
    name: string,
    text?: string,
}

const HeadBar = (props: Props) => {
    if (props.text) {
        return (
            <div className={componentStyle.headBar}>
                <div className={componentStyle.title}>{props.name}</div>
                <div className={componentStyle.text}>{props.text}</div>
            </div>
        )
    } else {
        return (
            <div className={componentStyle.headBar}>
                <div className={componentStyle.title}>{props.name}</div>
            </div>
        )
    }

}

export default HeadBar
