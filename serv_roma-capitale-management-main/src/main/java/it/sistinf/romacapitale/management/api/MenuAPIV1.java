package it.sistinf.romacapitale.management.api;

import io.swagger.v3.oas.annotations.Operation;
import it.sistinf.romacapitale.core.api.AbstractSqlAPI;
import it.sistinf.romacapitale.core.dto.RequestListDTO;
import it.sistinf.romacapitale.core.dto.ResponseDTO;
import it.sistinf.romacapitale.core.dto.ResponseListDTO;
import it.sistinf.romacapitale.integration.management.vo.MenuVO;
import it.sistinf.romacapitale.integration.management.vo.StrutturaVO;
import it.sistinf.romacapitale.management.domain.MenuDomain;
import it.sistinf.romacapitale.management.domain.StrutturaDomain;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@AllArgsConstructor
@RequestMapping("/api/v1/menu")
public class MenuAPIV1 extends AbstractSqlAPI {

    private final MenuDomain menuDomain;

    @Operation(summary = "Elenco menu", description = "Restituisce l'elenco dei menu in base ai filtri, ordinamenti e paginazione specificati")
    @GetMapping("/list")
    public ResponseListDTO<MenuVO> listMenus(
            @RequestParam(value = "filters", required = false) List<String> filtersList,
            @RequestParam(value = "sort", required = false) List<String> sortList,
            @RequestParam(value = "pageOffset", required = false) Integer pageOffset,
            @RequestParam(value = "pageSize", required = false) Integer pageSize
    ) {
        RequestListDTO<MenuVO> request = makePaginatedSearchRequest(filtersList, sortList, pageOffset, pageSize);
        return menuDomain.listMenus(request);
    }

    @Operation(summary = "Interrogazione Menu", description = "Interrogazione di un menu per id")
    @GetMapping("/{id}")
    public ResponseDTO<MenuVO> getMenu(@PathVariable @NotNull Long id) {
        return new ResponseDTO<>(menuDomain.getMenu(id));
    }

    @Operation(summary = "Inserimento Menu", description = "Inserimento di un menu")
    @PostMapping("/")
    public ResponseDTO<MenuVO> createMenu(@Valid @RequestBody MenuVO request) {
        return new ResponseDTO<>(menuDomain.createMenu(request));
    }

    @Operation(summary = "Modifica Menu", description = "Modifica di un menu")
    @PutMapping("/{id}")
    public ResponseDTO<MenuVO> updateMenu(@PathVariable Long id, @Valid @RequestBody MenuVO request) {
        request.setKey(id);
        return new ResponseDTO<>(menuDomain.updateMenu(request));
    }

    @Operation(summary = "Cancellazione Menu", description = "Cancellazione di un menu")
    @DeleteMapping("/{id}")
    public ResponseDTO<Boolean> deleteMenu(@PathVariable Long id) {
        return new ResponseDTO<>(menuDomain.deleteMenu(id));
    }
}

