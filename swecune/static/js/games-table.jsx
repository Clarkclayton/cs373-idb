var MoveRow = React.createClass({
    render: function(){
        var gm = this.props.game;

        return(
            <tr>
                <td>
                    <img className="move-sprite" id="img_type_text" src={gm.image}/>
                </td>
                <td>{gm.name}</td>
                <td>{gm.platform}</td>
                <td>{gm.developer}</td>
                <td>{gm.publisher}</td>
            </tr>
        );
    }
});

var TableRows = React.createClass({
    render: function(){
        var rows = this.props.data.map(function(gm){
            return (<MoveRow game={gm} key={gm.id}/>)
        });
        return(
            <tbody>
                {rows}
            </tbody>
        );
    }
});


var MoveTable = React.createClass({
    requestData: function(){
        $.ajax({
            url: "/ggmate",
            cache: true,
            success: function(data) {
                console.log("MOUNTED");
                console.log(data);
                data.map(function(gm){
                    gm.developer = gm.developers[0] ? gm.developers[0].name : "";
                    gm.publisher = gm.publishers[0] ? gm.publishers[0].name : "";
                    gm.platform = gm.platforms[0] ? gm.platforms[0].name : "";
                });
                this.setState({data: data, loaded: "true"});
                spinner.stop();
            }.bind(this),
            error: function(xhr, status, err){
                console.error("/ggmate", status, err.toString());
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
        if(n == 0){
            return;
        }
        var cols = [0, "name", "platform", "developer", "publisher"];
        var k = cols[n];
        var data = this.state.data;
        data.sort(function(a, b){
            if(a[k] == ""){
                return 1;
            }
            else if(b[k] == ""){
                return -1;
            }

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
                        <th id="sprite">Sprite</th>
                        <TableHead p={this} col="1" name="Name"/>
                        <TableHead p={this} col="2" name="Platform"/>
                        <TableHead p={this} col="3" name="Developer"/>
                        <TableHead p={this} col="4" name="Publisher"/>
                    </tr>
                </thead>
                <TableRows data={this.state.data.slice((this.state.page - 1) * 10, this.state.page * 10)}/>
            </table>
            <Paginator p={this} doRender={this.state.loaded} swidth="8"/>
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

/*
var handleClick = function(table, page){
    console.log(table);
    table.changePage(page);
};
*/

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
        return {width: width, current: 1, buttons: buttons, doRender: false}
    },

    handleClick: function(page){
        var buttons = Array(this.state.width);

        var margin = Math.floor(this.state.width / 2);
        var start = Math.max(1, page - margin);
        var end = Math.ceil(this.props.p.state.data.length / 10);
        var a = Math.ceil(this.props.p.state.data.length / 10);
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
        var nextButton = this.handleClick.bind(this, Math.min(Math.ceil(this.props.p.state.data.length / 10), this.state.current + 1));
        var rend = null;
        if(this.props.doRender == "true"){
            rend = (
            <nav className="poke-table">
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
    <MoveTable/>,
    document.getElementById('gamesdiv')
);
