package it.sistinf.romacapitale.management.repository;

import it.sistinf.romacapitale.core.persistence.sql.AbstractRepository;
import it.sistinf.romacapitale.management.entity.MenuEntity;
import org.springframework.stereotype.Repository;

@Repository
public class MenuRepository extends AbstractRepository<Long, MenuEntity> {

    public MenuRepository() {
        super(MenuEntity.class);
    }
}
