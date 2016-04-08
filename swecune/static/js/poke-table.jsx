var SLICE_WIDTH = 10;

var PokeRow = React.createClass({
    render: function(){
        var pk = this.props.pokemon;
        return(
            <tr>
                <td><a href={"/pokemon/" + pk.id}>
                    <img src={"/static/img/pokemon/pokemon_" + pk.id + ".png"}/></a>
                </td>
                <td data-value="{pk.id}">{pk.id}</td>
                <td><a href={"/pokemon/" + pk.id}>{pk.name}</a></td>
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
//this.setState({data: db_pokemon});
        $.ajax({
            url: "/api/min_pokemon",
            dataType: "json",
            cache: false,
            success: function(data) {
                console.log("MOUNTED");
                this.setState({data: data, loaded: "true"});
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
            page: 1,
            loaded: "false"
        })
    },

    changePage: function(p){
        console.log("page: " + p);
        this.setState({page: p});
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
            <table className="poke-table table">
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
                <TableRows data={this.state.data.slice((this.state.page - 1) * SLICE_WIDTH, this.state.page * SLICE_WIDTH)}/>
            </table>
            <Paginator p={this} swidth="9" doRender={this.state.loaded}/>
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


var doNothing = function(){
    return false;
}

var gk = 1;

var Paginator = React.createClass({
    getInitialState: function(){
        var width = parseInt(this.props.swidth);
        console.log("the width is: " + width);
        var buttons = Array(width);
        for(var i = 0; i < width; i++){
            var p_num = i + 1;
            var boundClick = this.handleClick.bind(this, p_num);
            var ln;
            if(p_num == 1){
                ln = <a onClick={doNothing} className="current-page">{p_num}</a>
            }
            else{
                ln = <a href="#" onClick={boundClick}>{p_num}</a>
            }
            gk++;
            buttons[i] = (<li key={gk}>
                            {ln}
                        </li>);
        }
        return {width: width, current: 1, buttons: buttons}
    },

    handleClick: function(page){
        var buttons = Array(this.state.width);

        var margin = Math.floor(this.state.width / 2);
        var start = Math.max(1, page - margin);
        var end = Math.ceil(this.props.p.state.data.length / SLICE_WIDTH);
        var a = Math.ceil(this.props.p.state.data.length / SLICE_WIDTH);
        console.log("a is: " + a);

        for(var i = 0; i < this.state.width; i++){
            var p_num = start + i;
            var boundClick = this.handleClick.bind(this, p_num);
            var ln;
            if(p_num == page){
                ln = <a onClick={doNothing} className="current-page">{p_num}</a>
            }
            else{
                ln = <a href="#" onClick={boundClick}>{p_num}</a>
            }
            if(p_num > end){
                ln = <a onClick={doNothing} className="current-page">.</a>
            }
            gk++;
            buttons[i] = (<li key={gk}>
                            {ln}
                        </li>);
        }
        this.props.p.changePage(page);
        this.setState({buttons: buttons, current: page});
    },

    render: function(){
        var prevButton = this.handleClick.bind(this, Math.max(1, this.state.current - 1));
        var nextButton = this.handleClick.bind(this, Math.min(Math.ceil(this.props.p.state.data.length / SLICE_WIDTH), this.state.current + 1));
        var rend = null;
        if(this.props.doRender == "true"){
            rend = (
            <nav className="text-center">
                <ul className="pagination">
                    <li>
                        <a href="#" aria-label="Previous" onClick={prevButton}>
                            <span aria-hidden="true">&laquo;</span>
                        </a>
                    </li>
                    {this.state.buttons}
                    <li>
                        <a href="#" aria-label="Next" onClick={nextButton}>
                            <span aria-hidden="true">&raquo;</span>
                        </a>
                    </li>
                </ul>
            </nav>)
        }
        return rend;
    }
});

ReactDOM.render(
    <PokeTable/>,
    document.getElementById('pokediv')
);
