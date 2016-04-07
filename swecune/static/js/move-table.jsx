var MoveRow = React.createClass({
    render: function(){
        var mv = this.props.move;
        return(
            <tr>
                <td><a href={"/move/" + mv.id}>{capitalize(mv.name)}</a></td>
                <td data-value="{mv.primary_type}"><a href={"/type/" + mv.primary_type}>
                    <img id="move_type_text_img" src={"/static/img/type_text_" + mv.primary_type + ".png"}/>
                </a></td>
                <td>{mv.power}</td>
                <td>{mv.accuracy}</td>
                <td>{mv.pp}</td>
            </tr>
        )
    }
});

var TableRows = React.createClass({
    render: function(){
        var rows = this.props.data.map(function(mv){
            return (<MoveRow move={mv} key={mv.id}/>)
        });
        return(
            <tbody>
                {rows}
            </tbody>
        );
    }
});

var MoveTable = React.createClass({
    requestData: function(offset, limit){
        $.ajax({
            url: "/api/move",
            data: {offset: offset, limit: limit},
            dataType: "json",
            cache: false,
            success: function(data) {
                console.log("MOUNTED");
                this.setState({data: data});
            }.bind(this),
            error: function(xhr, status, err){
                console.error("/api/move", status, err.toString());
            }.bind(this)
        });
    },

    componentDidMount: function(){
        console.log("component did mount");
        this.requestData(0, SLICE_WIDTH);
    },

    getInitialState: function(){
        return ({
            data: [],
        })
    },

    changePage: function(p){
        console.log("page: " + p);
        this.requestData((p - 1) * SLICE_WIDTH, SLICE_WIDTH);
    },

    render: function(){
        return(
            <div>
            <table className="poke-table sortable-theme-bootstrap" data-sortable>
                <thead>
                    <tr>
                        <th data-sortable="false">Sprite</th>
                        <th>Name</th>
                        <th>Power</th>
                        <th>Accuracy</th>
                        <th>PP</th>
                    </tr>
                </thead>
                <TableRows data={this.state.data}/>
            </table>
            <Paginator p={this}/>
            </div>
        )
    }
});

var handleClick = function(table, page){
    console.log(table);
    table.changePage(page);
}

var Paginator = React.createClass({
    render: function(){
        return(
            <nav>
               <ul className="pagination">
                   <li>
                       <a href="#" aria-label="Previous">
                       <span aria-hidden="true">&laquo;</span>
                       </a>
                   </li>
                   <li><a href="#" onClick={handleClick.bind(this, this.props.p, 1)}>1</a></li>
                   <li><a href="#" onClick={handleClick.bind(this, this.props.p, 2)}>2</a></li>
                   <li><a href="#" onClick={handleClick.bind(this, this.props.p, 3)}>3</a></li>
                   <li><a href="#" onClick={handleClick.bind(this, this.props.p, 4)}>4</a></li>
                   <li><a href="#" onClick={handleClick.bind(this, this.props.p, 5)}>5</a></li>
                   <li>
                       <a href="#" aria-label="Next">
                       <span aria-hidden="true">&raquo;</span>
                       </a>
                   </li>
               </ul>
           </nav>
        )
    }
});

ReactDOM.render(
    <MoveTable/>,
    document.getElementById('movediv')
)
