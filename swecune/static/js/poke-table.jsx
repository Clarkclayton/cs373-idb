var SLICE_WIDTH = 10;

var capitalize = function(s){
    return s[0].toUpperCase() + s.slice(1);
}

var PokeRow = React.createClass({
    render: function(){
        var pk = this.props.pokemon;
        return(
            <tr>
                <td><a href={"/pokemon/" + pk.id}>
                    <img src={"/static/img/pokemon/pokemon_" + pk.id + ".png"}/></a>
                </td>
                <td data-value="{pk.id}">{pk.id}</td>
                <td><a href={"/pokemon/" + pk.id}>{capitalize(pk.name)}</a></td>
                <td data-value="{pk.primary_type}"><a href={"/type/" + pk.primary_type}>
                    <img id="move_type_text_img" src={"/static/img/type_text_" + pk.primary_type + ".png"}/>
                </a></td>
                { pk.secondary_type ?
                <td data-value="{pk.secondary_type}">
                <a href={"/type/" + pk.secondary_type}>
                    <img id="move_type_text_img" src={"/static/img/type_text_" + pk.secondary_type + ".png"}/>
                </a>
                </td>
                :<td data-value="-1">""</td>}
                <td> {pk.average_stats} </td>
            </tr>
        )
    }
});

var TableRows = React.createClass({
    render: function(){
        var rows = this.props.data.map(function(pk){
            return (<PokeRow pokemon={pk} key={pk.id}/>)
        });
        return(
            <tbody>
                {rows}
            </tbody>
        );
    }
});

var PokeTable = React.createClass({
    requestData: function(){
        $.ajax({
            url: "/api/min_pokemon",
            dataType: "json",
            cache: false,
            success: function(data) {
                console.log("MOUNTED");
                this.setState({data: data});
            }.bind(this),
            error: function(xhr, status, err){
                console.error("/api/pokemon", status, err.toString());
            }.bind(this)
        });
    },

    componentDidMount: function(){
        console.log("component did mount");
        this.requestData();
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

    sortByColumn: function(n, ascending){
        n = parseInt(n);
        var cols = [0, "id", "name", "primary_type", "secondary_type", "average_stats"];
        var k = cols[n];
        var data = this.state.data;
        data.sort(function(a, b){
            if(a[k] < b[k]){
                return -1;
            }
            else if(a[k] > b[k]){
                return 1;
            }
            return 0;
        });
        if(!ascending){
            data.reverse();
        }
        this.setState({data: data});
    },

    render: function(){
        return(
            <div>
            <table className="poke-table">
                <thead>
                    <tr>
                        <th>Sprite</th>
                        <TableHead p={this} col="1" name="ID"/>
                        <TableHead p={this} col="2" name="Name"/>
                        <TableHead p={this} col="3" name="Primary Type"/>
                        <TableHead p={this} col="4" name="Secondary Type"/>
                        <TableHead p={this} col="5" name="Average Stats"/>
                    </tr>
                </thead>
                <TableRows data={this.state.data}/>
            </table>
            <Paginator p={this}/>
            </div>
        )
    }
});

var TableHead = React.createClass({
    getInitialState: function(){
        return {ascending: false};
    },
    sort: function(){
        this.props.p.sortByColumn(this.props.col, this.state.ascending);
        this.setState({ascending: !this.state.ascending});
    },
    render: function(){
        return(<th onClick={this.sort}>{this.props.name}</th>)
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
    <PokeTable/>,
    document.getElementById('pokediv')
);
