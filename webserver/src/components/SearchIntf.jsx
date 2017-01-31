import React from 'react';
import { inject, observer } from 'mobx-react';
import mobx from 'mobx'
import {Input, Button, Form} from 'antd'

const FormItem = Form.Item;

@inject('dataStore', 'viewStore')
class SearchIntf extends React.Component {
  constructor(props) {
    super()
    this.state = {search_terms: [""]}
  }

  componentDidMount() {
    
  }

  deleteEvent = (iRemove) => {
    return (e) => {
      this.setState({
        search_terms: this.state.search_terms.filter( (e, i) => i != iRemove)
      })
      
    }
  }

  handleSubmit = () => {
    this.props.viewStore.setSearches([...this.state.search_terms])
    this.props.dataStore.load(this.props.viewStore.granularity, this.props.viewStore.searches)
  }

  addEvent = () => {
    this.setState({
      search_terms: [...this.state.search_terms, ""]
    })
  }

  render() {
    return <div>
      <h2>Search</h2>
      <p>Search trends</p>
      {
        this.state.search_terms.map((term, i) => {
          return <span key={i} style={{"width": "100%"}}>
            <Input
              placeholder="trend"
              defaultValue={term}
              style={{
                "marginRight": "5px",
                "width": "60%"
              }}
              onChange={
                (e) => {
                  var state = [...this.state.search_terms]
                  state[i] = e.target.value
                  this.setState({
                    search_terms: state
                  })
                }
              }
            />
            { (i > 0) &&
              <Button
                type="ghost" 
                shape="circle" 
                icon="cross" 
                onClick={this.deleteEvent(i)}
              />
            }
          </span>
        })
      }
      <Button
          type="ghost" 
          shape="circle" 
          icon="plus" 
          onClick={this.addEvent}
        />
      <Button type="primary" onClick={this.handleSubmit}>
        Show trend
      </Button>
    </div>
  }
}

export default SearchIntf;