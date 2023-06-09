var dagcomponentfuncs = window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {};

dagcomponentfuncs.DMC_Button = function (props) {
    const { setData, data } = props;

    function onClick() {
        setData();
    }
    let leftIcon, rightIcon;
    if (props.leftIcon) {
        leftIcon = React.createElement(window.dash_iconify.DashIconify, {
            icon: props.leftIcon,
        });
    }
    if (props.rightIcon) {
        rightIcon = React.createElement(window.dash_iconify.DashIconify, {
            icon: props.rightIcon,
        });
    }
    return React.createElement(
        window.dash_mantine_components.Button,
        {
            onClick,
            variant: props.variant,
            color: props.color,
            leftIcon,
            rightIcon,
            radius: props.radius,
            style: props.style,
        },
        props.value
    );
};


dagcomponentfuncs.DCC_GraphClickData = function (props2) {
    const { setData2 } = props2;
    function setProps2() {
        const graphProps = arguments[0];
        if (graphProps['clickData']) {
            setData2(graphProps);
        }
    }
    return React.createElement(window.dash_core_components.Graph, {
        figure: props2.value,
        setProps2,
        style: { height: '100%' },
        config: { displayModeBar: false },
    });
};
