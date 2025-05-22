import * as React from 'react';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Stack from '@mui/material/Stack';
import SettingsRoundedIcon from '@mui/icons-material/SettingsRounded';
import HomeIcon from '@mui/icons-material/Home';
import StickyNote2Icon from '@mui/icons-material/StickyNote2';
import StickyNote2OutlinedIcon from '@mui/icons-material/StickyNote2Outlined';
import UpdateOutlinedIcon from '@mui/icons-material/UpdateOutlined';
import MailOutlineOutlinedIcon from '@mui/icons-material/MailOutlineOutlined';
import GavelOutlinedIcon from '@mui/icons-material/GavelOutlined';
import CurrencyExchangeOutlinedIcon from '@mui/icons-material/CurrencyExchangeOutlined';
import BlurOnOutlinedIcon from '@mui/icons-material/BlurOnOutlined';
import PeopleOutlineOutlinedIcon from '@mui/icons-material/PeopleOutlineOutlined';
import EngineeringOutlinedIcon from '@mui/icons-material/EngineeringOutlined';
import AttachEmailOutlinedIcon from '@mui/icons-material/AttachEmailOutlined';
import HandymanOutlinedIcon from '@mui/icons-material/HandymanOutlined';
import FileDownloadOutlinedIcon from '@mui/icons-material/FileDownloadOutlined';
import FileUploadOutlinedIcon from '@mui/icons-material/FileUploadOutlined';
import FlipOutlinedIcon from '@mui/icons-material/FlipOutlined';
import EventAvailableOutlinedIcon from '@mui/icons-material/EventAvailableOutlined';
import EventRepeatOutlinedIcon from '@mui/icons-material/EventRepeatOutlined';
import InventoryOutlinedIcon from '@mui/icons-material/InventoryOutlined';
import DescriptionOutlinedIcon from '@mui/icons-material/DescriptionOutlined';
import EventNoteOutlinedIcon from '@mui/icons-material/EventNoteOutlined';
import BorderColorOutlinedIcon from '@mui/icons-material/BorderColorOutlined';
import ListAltOutlinedIcon from '@mui/icons-material/ListAltOutlined';
import FactCheckIcon from '@mui/icons-material/FactCheck';
import ModeEditOutlineIcon from '@mui/icons-material/ModeEditOutline';
import NoteAltIcon from '@mui/icons-material/NoteAlt';
import FileUploadIcon from '@mui/icons-material/FileUpload';
import MonetizationOnIcon from '@mui/icons-material/MonetizationOn';
import DescriptionIcon from '@mui/icons-material/Description';
import AssuredWorkloadIcon from '@mui/icons-material/AssuredWorkload';
import CountertopsIcon from '@mui/icons-material/Countertops';
import EditNoteIcon from '@mui/icons-material/EditNote';
import ContentPasteGoIcon from '@mui/icons-material/ContentPasteGo';
import ChecklistIcon from '@mui/icons-material/Checklist';
import AccountBalanceIcon from '@mui/icons-material/AccountBalance';
import ImportContactsIcon from '@mui/icons-material/ImportContacts';
import RequestQuoteIcon from '@mui/icons-material/RequestQuote';
import AttachMoneyOutlinedIcon from '@mui/icons-material/AttachMoneyOutlined';
import PointOfSaleOutlinedIcon from '@mui/icons-material/PointOfSaleOutlined';
import LibraryBooksOutlinedIcon from '@mui/icons-material/LibraryBooksOutlined';
import WorkspacePremiumOutlinedIcon from '@mui/icons-material/WorkspacePremiumOutlined';
import AutoDeleteOutlinedIcon from '@mui/icons-material/AutoDeleteOutlined';
import RequestQuoteOutlinedIcon from '@mui/icons-material/RequestQuoteOutlined';
import LineStyleOutlinedIcon from '@mui/icons-material/LineStyleOutlined';
import AssignmentTurnedInOutlinedIcon from '@mui/icons-material/AssignmentTurnedInOutlined';
import AssignmentOutlinedIcon from '@mui/icons-material/AssignmentOutlined';
import ArticleIcon from '@mui/icons-material/Article';
import MiscellaneousServicesIcon from '@mui/icons-material/MiscellaneousServices';
import HomeRepairServiceIcon from '@mui/icons-material/HomeRepairService';
import HelpIcon from '@mui/icons-material/Help';
import clsx from 'clsx';
import { animated, useSpring } from '@react-spring/web';
import { styled, alpha } from '@mui/material/styles';
import { TransitionProps } from '@mui/material/transitions';
import Box from '@mui/material/Box';
import Collapse from '@mui/material/Collapse';
import Typography from '@mui/material/Typography';
import PriceCheckOutlinedIcon from '@mui/icons-material/PriceCheckOutlined';
import DevicesFoldOutlinedIcon from '@mui/icons-material/DevicesFoldOutlined';
import ReceiptOutlinedIcon from '@mui/icons-material/ReceiptOutlined';
import ReceiptLongOutlinedIcon from '@mui/icons-material/ReceiptLongOutlined';
import CalendarMonthOutlinedIcon from '@mui/icons-material/CalendarMonthOutlined';
import CalendarTodayOutlinedIcon from '@mui/icons-material/CalendarTodayOutlined';
import DeleteIcon from '@mui/icons-material/Delete';
import { RichTreeView } from '@mui/x-tree-view/RichTreeView';
import { treeItemClasses } from '@mui/x-tree-view/TreeItem';
import { useTreeItem2, UseTreeItem2Parameters } from '@mui/x-tree-view/useTreeItem2';
import {
  TreeItem2Checkbox,
  TreeItem2Content,
  TreeItem2IconContainer,
  TreeItem2Label,
  TreeItem2Root,
} from '@mui/x-tree-view/TreeItem2';
import { TreeItem2Icon } from '@mui/x-tree-view/TreeItem2Icon';
import { TreeItem2Provider } from '@mui/x-tree-view/TreeItem2Provider';
import { TreeItem2DragAndDropOverlay } from '@mui/x-tree-view/TreeItem2DragAndDropOverlay';
import { TreeViewBaseItem } from '@mui/x-tree-view/models';
import DashboardIcon from '@mui/icons-material/Dashboard';
import { Link, useNavigate } from 'react-router-dom';
import { useTreeViewApiRef } from '@mui/x-tree-view/hooks';

type ExtendedTreeItemProps = {
  id: string;
  label: string;
  icon?: React.ElementType;
  to?: string;
};


const ITEMS: TreeViewBaseItem<ExtendedTreeItemProps>[] = [
  {
    id: '1',
    label: 'Dashboard',
    icon: DashboardIcon,
    to: '/dashboard',
  },
  {
    id: '2',
    label: 'Facturação',
    icon: ReceiptLongOutlinedIcon,
    children: [
      {
        id: '2.1',
        label: 'Facturas',
        icon: ReceiptLongOutlinedIcon,
        to: '/fatura',
        children: [
          { id: '2.1.1', label: 'Nova Factura', icon: ReceiptLongOutlinedIcon, to: '/nova-fatura' },
          { id: '2.1.2', label: 'Factura Proforma', icon: StickyNote2Icon, to: '/nova-proforma' },
          { id: '2.1.3', label: 'Factura Recibo', icon: DescriptionOutlinedIcon, to: '/factura-recibo' },
          { id: '2.1.4', label: 'Nota Recibo', icon: DescriptionOutlinedIcon, to: '/nota-debito' },
          { id: '2.1.5', label: 'Autofacturacao', icon: DescriptionOutlinedIcon, to: '/autofacturacao' },
          { id: '2.1.6', label: 'Factura Global', icon: DescriptionOutlinedIcon, to: '/factura-global' },
          { id: '2.1.7', label: 'Guia Remessa', icon: DescriptionOutlinedIcon, to: '/guia-remessa' },
          { id: '2.1.8', label: 'Guia Transporte', icon: DescriptionOutlinedIcon, to: '/guia-transporte' },
          { id: '2.1.9', label: 'Envio de facturas', icon: MailOutlineOutlinedIcon, to: '/dashboard' },
          { id: '2.1.10', label: 'Histórico e acompanhamento', icon: UpdateOutlinedIcon, to: '/dashboard' },
          { id: '2.1.11', label: 'Lembretes automáticos', icon: StickyNote2OutlinedIcon, to: '/dashboard' },
        ],
      },
       {
        id: '2.2',
        label: 'Relatórios',
        icon: ReceiptLongOutlinedIcon,
        to: '/relatorios',
        children: [
          { id: '2.2.1', label: 'Relatório de Facturação', icon: ReceiptLongOutlinedIcon, to: '/relatorio-facturas' },
          { id: '2.2.2', label: 'Facturação por Item', icon: StickyNote2Icon, to: '/facturas-item' },
          { id: '2.2.3', label: 'Conta corrente de cliente', icon: DescriptionOutlinedIcon, to: '/contas-cliente' },
          { id: '2.2.4', label: 'Pagamentos em Falta', icon: DescriptionOutlinedIcon, to: '/pagamentos-falta' },
          { id: '2.2.5', label: 'Liquidação de Impostos', icon: DescriptionOutlinedIcon, to: '/liquidacao-impostos' },
          { id: '2.2.6', label: 'Mapa de Impostos', icon: DescriptionOutlinedIcon, to: '/mapa-impostos'},
          { id: '2.2.7', label: 'Relatório de Facturação por Gestores', icon: DescriptionOutlinedIcon, to: '/facturas-gestor' },
          { id: '2.2.8', label: 'Pagamentos Efectuados (Recibos)', icon: DescriptionOutlinedIcon, to: '/pagamentos-efectuados' },

        ],
      },
      {
        id: '2.3',
        label: 'Clientes e Fornecedores',
        icon: PeopleOutlineOutlinedIcon,
        children: [
          { id: '2.3.1', label: 'Clientes', icon: ReceiptLongOutlinedIcon, to: '/clientes' },
          { id: '2.3.2', label: 'Fornecedores', icon: StickyNote2Icon, to: '/suppliers' },
        ],
      },
      { id: '2.4', label: 'Produtos e Serviços', icon: BlurOnOutlinedIcon, to: '/dashboard', children: [
          { id: '2.4.1', label: 'Productos', icon: BlurOnOutlinedIcon, to: '/listagem-produtos' },
          { id: '2.4.2', label: 'Serviços', icon: BlurOnOutlinedIcon, to: '/services' },
      ]},
      { id: '2.5', label: 'Gestão de Pagamentos', icon: CurrencyExchangeOutlinedIcon, to: '/dashboard' },
      { id: '2.6', label: 'Impostos e Descontos', icon: RequestQuoteIcon, to: '/dashboard' },
    ],
  },
  {
    id: '3',
    label: 'Diário',
    icon: FactCheckIcon,
    children: [
      { id: '3.1', label: 'Notas', icon: ModeEditOutlineIcon, to: '/dashboard' },
      { id: '3.2', label: 'Assentos', icon: NoteAltIcon, to: '/dashboard' },
      { id: '3.3', label: 'Carregamento rápido', icon: FileUploadIcon, to: '/dashboard' },
      { id: '3.4', label: 'Contabilidade', icon: MonetizationOnIcon, to: '/dashboard' },
      { id: '3.5', label: 'Extratos rápidos', icon: DescriptionIcon, to: '/dashboard' },
      { id: '3.6', label: 'Conciliação bancária', icon: AssuredWorkloadIcon, to: '/dashboard' },
    ],
  },
  {
    id: '4',
    label: 'Lançamentos',
    icon: ContentPasteGoIcon,
    children: [
      { id: '4.1', label: 'Imobilizado', icon: CountertopsIcon, to: '/dashboard' },
      { id: '4.2', label: 'Amortização', icon: EditNoteIcon, to: '/dashboard' },
    ],
  },
  {
    id: '5',
    label: 'Plano Contable',
    icon: ChecklistIcon,
    children: [
      { id: '5.1', label: 'Plano Contable', icon: ChecklistIcon, to: '/dashboard' },
      { id: '5.2', label: 'Importar plano de contas', icon: CountertopsIcon, to: '/dashboard' },
      { id: '5.3', label: 'Apagar contas', icon: DeleteIcon, to: '/dashboard' },
      { id: '5.4', label: 'Ajuda do plano contabilístico', icon: HelpIcon, to: '/dashboard' },
    ],
  },
  {
    id: '6',
    label: 'Tesouraria',
    icon: AccountBalanceIcon,
    children: [
      { id: '6.1', label: 'Vencimento de cobrança', icon: CalendarMonthOutlinedIcon, to: '/dashboard' },
      { id: '6.2', label: 'Vencimento de pagamento', icon: CalendarTodayOutlinedIcon, to: '/dashboard' },
      { id: '6.3', label: 'Recibos', icon: ReceiptOutlinedIcon, to: '/dashboard' },
      { id: '6.4', label: 'Cheques e Livranças', icon: DevicesFoldOutlinedIcon, to: '/dashboard' },
      { id: '6.5', label: 'Movimentos de Caixa', icon: PointOfSaleOutlinedIcon, to: '/dashboard' },
      { id: '6.6', label: 'Receitas e Despesas', icon: ReceiptLongOutlinedIcon, to: '/dashboard' },
      { id: '6.7', label: 'Revisão de Tesouraria', icon: PriceCheckOutlinedIcon, to: '/dashboard' },
      { id: '6.8', label: 'Moedas estrangeiras', icon: AttachMoneyOutlinedIcon, to: '/dashboard' },
    ],
  },
  {
    id: '7',
    label: 'Livros e Contas Anuais',
    icon: ImportContactsIcon,
    children: [
      { id: '7.1', label: 'Diário', icon: FactCheckIcon, to: '/dashboard' },
      { id: '7.2', label: 'Mayor', icon: LibraryBooksOutlinedIcon, to: '/dashboard' },
      { id: '7.3', label: 'Relatório de retenção', icon: ListAltOutlinedIcon, to: '/dashboard' },
      { id: '7.4', label: 'Livros - Registo de fatura', icon: BorderColorOutlinedIcon, to: '/dashboard' },
      { id: '7.5', label: 'Relatório de retenção', icon: AssignmentOutlinedIcon, to: '/dashboard' },
      { id: '7.6', label: 'Balanços de Comprovação', icon: AssignmentOutlinedIcon, to: '/dashboard' },
      { id: '7.7', label: 'Balanços de Somas e Saldos', icon: AssignmentOutlinedIcon, to: '/dashboard' },
      { id: '7.8', label: 'Balanços de Situação', icon: AssignmentOutlinedIcon, to: '/dashboard' },
      { id: '7.9', label: 'Perdas e Ganhos', icon: AssignmentOutlinedIcon, to: '/dashboard' },
      { id: '7.10', label: 'Situação das Receitas e despesas reconhecidas', icon: LineStyleOutlinedIcon, to: '/dashboard' },
      { id: '7.11', label: 'Situação total e alterações', icon: LineStyleOutlinedIcon, to: '/dashboard' },
      { id: '7.12', label: 'Situação do fluxo de caixa', icon: LineStyleOutlinedIcon, to: '/dashboard' },
      { id: '7.13', label: 'Memória', icon: LineStyleOutlinedIcon, to: '/dashboard' },
      { id: '7.14', label: 'Relatório de Gestão', icon: LineStyleOutlinedIcon, to: '/dashboard' },
      { id: '7.15', label: 'Certificado de contas', icon: LineStyleOutlinedIcon, to: '/dashboard' },
      { id: '7.16', label: 'Registo de parceiro', icon: LineStyleOutlinedIcon, to: '/dashboard' },
      { id: '7.17', label: 'Minutos da conta', icon: LineStyleOutlinedIcon, to: '/dashboard' },
      { id: '7.18', label: 'Legalização de livros', icon: LineStyleOutlinedIcon, to: '/dashboard' },
      { id: '7.19', label: 'Indices financeiros', icon: LineStyleOutlinedIcon, to: '/dashboard' },
    ],
  },
  {
    id: '8',
    label: 'Impostos',
    icon: GavelOutlinedIcon,
    children: [
      { id: '8.1', label: 'Modelo 130', icon: RequestQuoteOutlinedIcon, to: '/dashboard' },
      { id: '8.2', label: 'Modelo 303', icon: RequestQuoteOutlinedIcon, to: '/dashboard' },
      { id: '8.3', label: 'Modelo 390', icon: RequestQuoteOutlinedIcon, to: '/dashboard' },
      { id: '8.4', label: 'Modelo 347', icon: RequestQuoteOutlinedIcon, to: '/dashboard' },
      { id: '8.5', label: 'Modelo 349', icon: RequestQuoteOutlinedIcon, to: '/dashboard' },
      { id: '8.6', label: 'Imposto empresas', icon: RequestQuoteOutlinedIcon, to: '/dashboard' },
    ],
  },
  {
    id: '9',
    label: 'Exercícios',
    icon: MiscellaneousServicesIcon,
    children: [
      { id: '9.1', label: 'Exercícios de contabilidade', icon: EventNoteOutlinedIcon, to: '/dashboard' },
      { id: '9.2', label: 'Alterar exercícios', icon: EventRepeatOutlinedIcon, to: '/dashboard' },
      { id: '9.3', label: 'Fecho/Abertura de Exercícios', icon: FlipOutlinedIcon, to: '/dashboard' },
      { id: '9.4', label: 'Assento de abertura', icon: EventAvailableOutlinedIcon, to: '/dashboard' },
    ],
  },
  {
    id: '10',
    label: 'Utilitários',
    icon: HomeRepairServiceIcon,
    children: [
      { id: '10.1', label: 'Suporte', icon: EngineeringOutlinedIcon, to: '/dashboard' },
      { id: '10.2', label: 'Mailings', icon: AttachEmailOutlinedIcon, to: '/dashboard' },
      { id: '10.3', label: 'Ferramentas', icon: HandymanOutlinedIcon, to: '/dashboard' },
      { id: '10.4', label: 'Certificados eletrónicos', icon: WorkspacePremiumOutlinedIcon, to: '/dashboard' },
      { id: '10.5', label: 'Importar', icon: FileUploadOutlinedIcon, to: '/import' },
      { id: '10.6', label: 'Exportar', icon: FileDownloadOutlinedIcon, to: '/dashboard' },
    ],
  },
];


const secondaryListItems = [
  { text: 'Settings', icon: <SettingsRoundedIcon />,to: '/settings'  },
];


function DotIcon() {
  return (
    <Box
      sx={{
        width: 6,
        height: 6,
        borderRadius: '70%',
        bgcolor: 'warning.main',
        display: 'inline-block',
        verticalAlign: 'middle',
        zIndex: 1,
        mx: 1,
      }}
    />
  );
}

declare module 'react' {
  interface CSSProperties {
    '--tree-view-color'?: string;
    '--tree-view-bg-color'?: string;
  }
}

const StyledTreeItemRoot = styled(TreeItem2Root)(({ theme }) => ({
  color: theme.palette.grey[400],
  position: 'relative',
  [`& .${treeItemClasses.groupTransition}`]: {
    marginLeft: theme.spacing(3.5),
  },
  ...theme.applyStyles('light', {
    color: theme.palette.grey[800],
  }),
})) as unknown as typeof TreeItem2Root;

const CustomTreeItemContent = styled(TreeItem2Content)(({ theme }) => ({
  flexDirection: 'row-reverse',
  borderRadius: theme.spacing(0.7),
  marginBottom: theme.spacing(0.5),
  marginTop: theme.spacing(0.5),
  padding: theme.spacing(0.5),
  paddingRight: theme.spacing(1),
  paddingLeft: '5px', // Ajustar paddingLeft a 5px
  fontWeight: 500,
  
  [`&.Mui-expanded `]: {
    '&:not(.Mui-focused, .Mui-selected, .Mui-selected.Mui-focused) .labelIcon': {
      color: theme.palette.primary.dark,
      ...theme.applyStyles('light', {
        color: theme.palette.primary.main,
      }),
    },
    '&::before': {
      content: '""',
      display: 'block',
      position: 'absolute',
      left: '16px',
      top: '44px',
      height: 'calc(100% - 48px)',
      width: '1.5px',
      backgroundColor: theme.palette.grey[700],
      ...theme.applyStyles('light', {
        backgroundColor: theme.palette.grey[300],
      }),
    },
  },
  '&:hover': {
    backgroundColor: alpha(theme.palette.primary.main, 0.1),
    color: 'white',
    ...theme.applyStyles('light', {
      color: theme.palette.primary.main,
    }),
  },
  [`&.Mui-focused, &.Mui-selected, &.Mui-selected.Mui-focused`]: {
    backgroundColor: theme.palette.primary.dark,
    color: theme.palette.primary.contrastText,
    ...theme.applyStyles('light', {
      backgroundColor: theme.palette.primary.main,
    }),
  },
}));

const AnimatedCollapse = animated(Collapse);

function TransitionComponent(props: TransitionProps) {
  const style = useSpring({
    to: {
      opacity: props.in ? 1 : 0,
      transform: `translate3d(0,${props.in ? 0 : 20}px,0)`,
    },
  });

  return <AnimatedCollapse style={style} {...props} />;
}

const StyledTreeItemLabelText = styled(Typography)({
  color: 'inherit',
  fontWeight: 500,
}) as unknown as typeof Typography;

interface CustomLabelProps {
  children: React.ReactNode;
  icon?: React.ElementType;
  expandable?: boolean;
}

function CustomLabel({
  icon: Icon,
  expandable,
  children,
  ...other
}: CustomLabelProps) {
  return (
    <TreeItem2Label
      {...other}
      sx={{
        display: 'flex',
        alignItems: 'center',
      }}
    >
      {Icon && (
        <Box
          component={Icon}
          className="labelIcon"
          color="inherit"
          sx={{ mr: 1, fontSize: '1.2rem' }}
        />
      )}

      <StyledTreeItemLabelText variant="body2">{children}</StyledTreeItemLabelText>
      {expandable && <DotIcon />}
    </TreeItem2Label>
  );
}

const isExpandable = (reactChildren: React.ReactNode) => {
  if (Array.isArray(reactChildren)) {
    return reactChildren.length > 0 && reactChildren.some(isExpandable);
  }
  return Boolean(reactChildren);
};

interface CustomTreeItemProps
  extends Omit<UseTreeItem2Parameters, 'rootRef'>,
    Omit<React.HTMLAttributes<HTMLLIElement>, 'onFocus'> {}

const CustomTreeItem = React.forwardRef(function CustomTreeItem(
  props: CustomTreeItemProps,
  ref: React.Ref<HTMLLIElement>,
) {
  const { id, itemId, label, disabled, children, ...other } = props;

  const {
    getRootProps,
    getContentProps,
    getIconContainerProps,
    getCheckboxProps,
    getLabelProps,
    getGroupTransitionProps,
    getDragAndDropOverlayProps,
    status,
    publicAPI,
  } = useTreeItem2({ id, itemId, children, label, disabled, rootRef: ref });

  const item = publicAPI.getItem(itemId);
  const expandable = isExpandable(children);
  const icon = item.icon;

  return (
    <TreeItem2Provider itemId={itemId}>
      <StyledTreeItemRoot {...getRootProps(other)}>
        <CustomTreeItemContent
          {...getContentProps({
            className: clsx('content', {
              'Mui-expanded': status.expanded,
              'Mui-selected': status.selected,
              'Mui-focused': status.focused,
              'Mui-disabled': status.disabled,
            }),
          })}
        >
          <TreeItem2IconContainer {...getIconContainerProps()}>
            <TreeItem2Icon status={status} />
          </TreeItem2IconContainer>
          <TreeItem2Checkbox {...getCheckboxProps()} />
          <CustomLabel
            {...getLabelProps({ icon, expandable: expandable && status.expanded })}
          />
          <TreeItem2DragAndDropOverlay {...getDragAndDropOverlayProps()} />
        </CustomTreeItemContent>
        {children && <TransitionComponent {...getGroupTransitionProps()} />}
      </StyledTreeItemRoot>
    </TreeItem2Provider>
  );
});

const MenuContent = () => {
  const navigate = useNavigate();
  const apiRef = useTreeViewApiRef();

  const handleSelectedItemsChange = (
    event: React.SyntheticEvent,
    itemIds: string | null
  ) => {
    if (!itemIds) return;
    
    const selectedItem = apiRef.current?.getItem(itemIds);
    
    if (selectedItem?.to) {
      navigate(selectedItem.to);
    }
  };

  return (
<Stack sx={{ flexGrow: 1, p: 1, justifyContent: 'space-between' }}>
<RichTreeView
      items={ITEMS}
      apiRef={apiRef}
      onSelectedItemsChange={handleSelectedItemsChange}
      multiSelect={false}
      defaultExpandedItems={['1', '1.1']}
      defaultSelectedItems="1.1"
      sx={{ height: 'fit-content', flexGrow: 1, maxWidth: 400, overflowY: 'auto' }}
      slots={{ item: CustomTreeItem }}
    />
      <List dense>
        {secondaryListItems.map((item, index) => (
          <ListItem key={index} disablePadding sx={{ display: 'block' }}>
            <ListItemButton component={Link} to={item.to} >
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Stack>
  );
}
export default MenuContent;