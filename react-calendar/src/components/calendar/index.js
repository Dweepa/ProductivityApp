import React, { useState } from "react";
import moment from "moment";
import { range } from "moment-range";
import "./calendar.css";

class NewComponent extends React.Component {
    constructor(props) {
    super(props);
    this.state = {
    title: '',
    description: '',
    course: '',
    team: '',
    section: '',
    };

//    @Input() date: string;
    console.log('props',this.state)
    this.handleSubmit = this.handleSubmit.bind(this);
    this.title = this.title.bind(this);
    this.course = this.course.bind(this);
    this.section = this.section.bind(this);
    this.team = this.team.bind(this);
    this.description = this.description.bind(this);

}
    title(e){
       this.setState({title: e.target.value});
//       console.log(this.state.title);
    }
    description(e){
       this.setState({description: e.target.value});
    }
    course(e){
       this.setState({course: e.target.value});
    }
    section(e){
       this.setState({section: e.target.value});
    }
    team(e){
       this.setState({team: e.target.value});
    }

    handleSubmit(event)
    {
        event.preventDefault();
        console.log(this.state);
        const dict = {'title':this.state.title,
        'description':this.state.description,
        'course':this.state.course,
        'section':this.state.section,
         'team':this.state.team,
         'd':this.props.d,
         'm':this.props.m,
         'y':this.props.y
         };
        fetch("http://127.0.0.1:5000/add", {method:"POST",
        headers: {
         'Accept': 'application/json',
         'Content-Type': 'application/json',
         },
         body:JSON.stringify(dict)})
        .then(res=>res.json())
        .then(res => {
        console.log(res);

        })
    }

      render() {
        return (
          <div className="jumbotron p-5">
          <h2> Add event </h2>
            <form onSubmit={this.handleSubmit}>
              <div class="form-group">
                <input name='title' onChange={this.title} type="text" className="form-control" placeholder="Title" />
              </div>

              <div class="form-group">
                <select name='course' onChange={this.course}>
                   <option>Choose a course</option>
                  <option>Software Engg</option>
                  <option>Big data</option>
                  <option>Cloud Computing</option>
                </select>
              </div>

              <div class="form-group">
                <select name='section' onChange={this.section}>
                  <option>Choose a section</option>
                  <option>A</option>
                  <option>B</option>
                  <option>C</option>
                </select>
              </div>

              <div class="form-group">
                <select name='team' onChange={this.team}>
                  <option>Choose a team</option>
                  <option>1</option>
                  <option>2</option>
                  <option>3</option>
                  <option>4</option>
                  <option>5</option>
                </select>
              </div>

              <div class="form-group">
                <label>Description</label>
                <textarea name='description' onChange={this.description} class="form-control" rows="3"></textarea>
              </div>

              <input type="submit" value="Add event"/>
            </form>
          </div>
        );
      }
}

function EventList (props) {
  const data1 = props.data;
  const listitems = data1.map((number) =>
  <div className='p-0'>
    <p className='bg-primary text-white p-2 rounded text-center'>{number.event.type}</p>
    <div className="row text-center">
        <div className='text-info col-sm'  style={{"fontSize":"12.5px","margin-left":"0px"}}>
            <p className='text-secondary' style={{"marginBottom":"1px"}}>Course</p>
            <p> {number.event.course}</p>
        </div>
        <div className='text-info col-sm' style={{"fontSize":"12.5px","margin-left":"0px"}}>
            <p className='text-secondary' style={{"marginBottom":"1px"}}>Section</p>
            <p>{number.event.section}</p>
        </div>
        <div className='text-info col-sm' style={{"fontSize":"12.5px","margin-left":"0px"}}>
            <p className='text-secondary' style={{"marginBottom":"1px"}}>Team</p>
            <p> {number.event.team}</p>
        </div>
    </div>
    <p className='bg-light text-muted p-2'>{number.event.description}</p>
    <hr style={{"marginTop":"25px","marginBottom":"25px"}}/>
  </div>
  );
  return (
    <div>{listitems}</div>
  );
  }
export default class Calendar extends React.Component {
  weekdayshort = moment.weekdaysShort();

  state = {
    showYearTable: false,
    showMonthTable: false,
    showDateTable: true,
    dateObject: moment(),
    allmonths: moment.months(),
    selectedDay: null,
    selectedMonth: null,
    selectedYear: null,
    clicked: false,
    data:null
  };

  handleClick = () => {
      this.setState({
        clicked: true
      });
    };

  daysInMonth = () => {
    return this.state.dateObject.daysInMonth();
  };
  year = () => {
    return this.state.dateObject.format("Y");
  };
  currentDay = () => {
    return this.state.dateObject.format("D");
  };
  firstDayOfMonth = () => {
    let dateObject = this.state.dateObject;
    let firstDay = moment(dateObject)
      .startOf("month")
      .format("d"); // Day of week 0...1..5...6
    return firstDay;
  };
  month = () => {
    if(this.state.data){
//    console.log("month",this.state.data);
  }
    var m = this.state.dateObject.format("MMMM");
    return m;
  };
  showMonth = (e, month) => {
    this.setState({
      showMonthTable: !this.state.showMonthTable,
     showDateTable: !this.state.showDateTable
    });
  };
  setMonth = month => {
    let monthNo = this.state.allmonths.indexOf(month);
    let dateObject = Object.assign({}, this.state.dateObject);
    dateObject = moment(dateObject).set("month", monthNo);
    this.setState({
      dateObject: dateObject,
      showMonthTable: !this.state.showMonthTable,
      showDateTable: !this.state.showDateTable
    });
  };
  MonthList = props => {
    let months = [];
    props.data.map(data => {
      months.push(
        <td
          key={data}
          className="calendar-month"
          onClick={e => {
            this.setMonth(data);
          }}
        >
          <span>{data}</span>
        </td>
      );
    });
    let rows = [];
    let cells = [];

    months.forEach((row, i) => {
      if (i % 3 !== 0 || i == 0) {
        cells.push(row);
      } else {
        rows.push(cells);
        cells = [];
        cells.push(row);
      }
    });
    rows.push(cells);
    let monthlist = rows.map((d, i) => {
      return <tr>{d}</tr>;
    });

    return (
      <table className="calendar-month">
        <thead>
          <tr>
            <th colSpan="4">Select a Month</th>
          </tr>
        </thead>
        <tbody>{monthlist}</tbody>
      </table>
    );
  };
  showYearTable = e => {
    this.setState({
      showYearTable: !this.state.showYearTable,
      showDateTable: !this.state.showDateTable
    });
  };

  onPrev = () => {
    let curr = "";
    if (this.state.showYearTable === true) {
      curr = "year";
    } else {
      curr = "month";
    }
    this.setState({
      dateObject: this.state.dateObject.subtract(1, curr)
    });
  };
  onNext = () => {
    let curr = "";
    if (this.state.showYearTable === true) {
      curr = "year";
    } else {
      curr = "month";
    }
    this.setState({
      dateObject: this.state.dateObject.add(1, curr)
    });
  };
  setYear = year => {
//    console.log("setYear", year);
    let dateObject = Object.assign({}, this.state.dateObject);
    dateObject = moment(dateObject).set("year", year);
    this.setState({
      dateObject: dateObject,
      showMonthTable: !this.state.showMonthTable,
      showYearTable: !this.state.showYearTable
    });
  };
  onYearChange = e => {
//    console.log("onYearChange ",e.target.value);
    this.setYear(e.target.value);
  };
  getDates(startDate, stopDate) {
    var dateArray = [];
    var currentDate = moment(startDate);
    var stopDate = moment(stopDate);
    while (currentDate <= stopDate) {
      dateArray.push(moment(currentDate).format("YYYY"));
      currentDate = moment(currentDate).add(1, "year");
    }
    return dateArray;
  }
  YearTable = props => {
    let months = [];
    let nextten = moment()
      .set("year", props)
      .add("year", 12)
      .format("Y");

    let tenyear = this.getDates(props, nextten);

    tenyear.map(data => {
      months.push(
        <td
          key={data}
          className="calendar-month"
          onClick={e => {
            this.setYear(data);
          }}
        >
          <span>{data}</span>
        </td>
      );
    });
    let rows = [];
    let cells = [];

    months.forEach((row, i) => {
      if (i % 3 !== 0 || i == 0) {
        cells.push(row);
      } else {
        rows.push(cells);
        cells = [];
        cells.push(row);
      }
    });
    rows.push(cells);
    let yearlist = rows.map((d, i) => {
      return <tr>{d}</tr>;
    });

    return (
      <table className="calendar-month">
        <thead>
          <tr>
            <th colSpan="4">Select a Yeah</th>
          </tr>
        </thead>
        <tbody>{yearlist}</tbody>
      </table>
    );
  };
  onDayClick = (e, d) => {
    this.setState(
      {
        selectedDay: d,
        selectedMonth: this.state.dateObject.format("MMMM"),
        selectedYear: this.state.dateObject.format("Y"),
        clicked:true
      },
      () => {
        var day = this.state.selectedDay;
        var mon = this.state.dateObject.format("MMMM");
        var yea = this.state.dateObject.format("Y");
//        console.log(day,mon,yea);

        fetch("http://127.0.0.1:5000/show/"+day+'/'+mon+'/'+yea).then(res => res.json().then(data1 => {this.setState({data: data1['output']});}));

      }
    );
  };
  render() {
    let weekdayshortname = this.weekdayshort.map(day => {
      return <th key={day}>{day}</th>;
    });
    let blanks = [];
    for (let i = 0; i < this.firstDayOfMonth(); i++) {
      blanks.push(<td className="calendar-day empty">{""}</td>);
    }
    let daysInMonth = [];
    for (let d = 1; d <= this.daysInMonth(); d++) {
      let currentDay = d == this.currentDay() ? "today" : "";
      daysInMonth.push(
        <td key={d} className={`calendar-day ${currentDay}`}>
          <span
            onClick={e => {
              this.onDayClick(e, d);
            }}
          >
            {d}
          </span>
        </td>
      );
    }
    var totalSlots = [...blanks, ...daysInMonth];
    let rows = [];
    let cells = [];

    totalSlots.forEach((row, i) => {
      if (i % 7 !== 0) {
        cells.push(row);
      } else {
        rows.push(cells);
        cells = [];
        cells.push(row);
      }
      if (i === totalSlots.length - 1) {
        // let insertRow = cells.slice();
        rows.push(cells);
      }
    });

    let daysinmonth = rows.map((d, i) => {
      return <tr>{d}</tr>;
    });

    return (
      <div className="row">
          <div className = "col-sm p-5">
              <div className="tail-datetime-calendar">
                <div className="calendar-navi">
                  <span
                    onClick={e => {
                      this.onPrev();
                    }}
                    className="calendar-button button-prev"
                  />
                  {!this.state.showMonthTable && (
                    <span
                      onClick={e => {
                        this.showMonth();
                      }}
                      className="calendar-label"
                    >
                      {this.month()}
                    </span>
                  )}
                  <span className="calendar-label" onClick={e => this.showYearTable()}>
                    {this.year()}
                  </span>
                   <span
                  onClick={e => {
                    this.onNext();
                  }}
                  className="calendar-button button-next"
                />
                </div>

                <div className="calendar-date">
                  {this.state.showYearTable && <this.YearTable props={this.year()} />}
                  {this.state.showMonthTable && (
                    <this.MonthList data={moment.months()} />
                  )}
                </div>

                {this.state.showDateTable && (
                  <div className="calendar-date">
                    <table className="calendar-day">
                      <thead>
                        <tr>{weekdayshortname}</tr>
                      </thead>
                      <tbody>{daysinmonth}</tbody>
                    </table>
                  </div>
                )}
              </div>
          </div>

         <div className="col-sm container p-5" style={{"marginTop":"0px","marginLeft":"150px"}}>
          {this.state.clicked ? ( <div className="jumbotron p-5"><h1 className='text-center'>{this.state.selectedDay} {this.state.selectedMonth} {this.state.selectedYear}</h1></div>) : null}
         {this.state.data? <div className="jumbotron p-5"> <EventList className='p-0 m-1' data={this.state.data}/> </div>:null}
         </div>

         <div className = 'col-sm container p-5' style={{"marginTop":"0px"}}>
         <div style={{"marginRight":"80px", "margin-Right":"0px","position":"fixed"}}>
          {this.state.clicked ? (<NewComponent d={this.state.selectedDay} m={this.state.selectedMonth} y={this.state.selectedYear} />):null}
         </div>
         </div>
    </div>
    );
  }
}
